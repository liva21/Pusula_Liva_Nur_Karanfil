import re
from typing import List
import numpy as np
import pandas as pd

# =========================
# Genel metin normalizasyon
# =========================

def normalize_whitespace(text):
    """Birden fazla boşluğu tek boşluğa indirir, baş/son boşlukları kırpar."""
    if pd.isna(text):
        return np.nan
    return re.sub(r"\s+", " ", str(text).strip())

def normalize_cinsiyet(val):
    """Cinsiyet değerlerini standart biçime çevirir: Erkek / Kadin / Diger."""
    if pd.isna(val):
        return np.nan
    s = str(val).strip().lower()
    mapping = {
        "e": "Erkek", "erkek": "Erkek", "male": "Erkek", "m": "Erkek",
        "k": "Kadin", "kadın": "Kadin", "kadin": "Kadin", "female": "Kadin", "f": "Kadin",
        "other": "Diger", "diğer": "Diger", "diger": "Diger", "o": "Diger",
    }
    return mapping.get(s, normalize_whitespace(val))

def normalize_kangrubu(val):
    """Kan grubunu (A,B,AB,0 ve +/-) standartlaştırır. Örn: 'A Rh Pozitif' -> 'A+'."""
    if pd.isna(val):
        return np.nan
    s = normalize_whitespace(val).upper()
    s = (s.replace("RH", "")
           .replace("POZITIF", "+").replace("POZİTİF", "+").replace("POZ", "+")
           .replace("NEGATIF", "-").replace("NEGATİF", "-").replace("NEG", "-")
           .replace(" ", "").replace("(", "").replace(")", "")
           .replace("RHPOS", "+").replace("RHNEG", "-")
           .replace("O", "0"))
    m = re.match(r"^(A|B|AB|0)(\+|-)?$", s)
    if m:
        base, rh = m.group(1), (m.group(2) or "")
        return f"{base}{rh}" if rh else base
    return s

def split_multilabel(cell):
    """Virgül/noktalı virgül/çizgi vb. ile ayrılmış çok-değerli metinleri listeye çevirir."""
    if pd.isna(cell):
        return []
    parts = re.split(r"[;,/]", str(cell))
    out = []
    for p in parts:
        p2 = normalize_whitespace(p)
        if p2:
            out.append(p2.lower())
    return out

def standardize_text_columns(df: pd.DataFrame, text_cols: List[str] = None) -> pd.DataFrame:
    """Temel metin sütunlarını normalize eder ve multi-label alanlar için __list sütunları üretir."""
    default_cols = [
        "KanGrubu", "Uyruk", "Bolum", "TedaviAdi",
        "Alerji", "KronikHastalik", "Tanilar", "UygulamaYerleri", "Cinsiyet"
    ]
    cols = text_cols or [c for c in default_cols if c in df.columns]
    for c in cols:
        df[c] = df[c].apply(normalize_whitespace)
    if "Cinsiyet" in df.columns:
        df["Cinsiyet"] = df["Cinsiyet"].apply(normalize_cinsiyet)
    if "KanGrubu" in df.columns:
        df["KanGrubu"] = df["KanGrubu"].apply(normalize_kangrubu)

    for c in ["KronikHastalik", "Alerji", "Tanilar", "UygulamaYerleri"]:
        if c in df.columns:
            df[f"{c}__list"] = df[c].apply(split_multilabel)
    return df

def winsorize_series(s: pd.Series, lower_q=0.01, upper_q=0.99) -> pd.Series:
    """Uç değerleri kırpmak için basit winsorization uygular."""
    s = pd.to_numeric(s, errors="coerce")
    if s.dropna().empty:
        return s
    lo, hi = s.quantile(lower_q), s.quantile(upper_q)
    return s.clip(lower=lo, upper=hi)

# =========================
# Hedef & süre dönüştürücü
# =========================

def normalize_tedavi_suresi(val):
    """
    TedaviSuresi'ni (seans sayısı) metinden sayıya çevirir.
    Desteklenen örnekler:
      - '10' / '10 seans'  -> 10
      - '3-5' / '3 – 5'    -> 4 (ortalama)
      - '10x3' / '10×3'    -> 30 (çarpım)
      - '15+'              -> 15
    """
    if pd.isna(val):
        return np.nan
    s = str(val).lower().strip()
    s = s.replace(",", ".")
    s = re.sub(r"\s*seans\s*", " ", s)
    s = re.sub(r"\s*\+\s*$", "", s)

    # Çarpım kalıbı: 10x3
    m_mul = re.search(r"(\d+(?:\.\d+)?)\s*[x×]\s*(\d+(?:\.\d+)?)", s)
    if m_mul:
        a = float(m_mul.group(1)); b = float(m_mul.group(2))
        return a * b

    # Aralık kalıbı: 3-5
    m_rng = re.search(r"(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)", s)
    if m_rng:
        a = float(m_rng.group(1)); b = float(m_rng.group(2))
        return (a + b) / 2.0

    # Metin içindeki ilk sayı
    m = re.search(r"(\d+(?:\.\d+)?)", s)
    if m:
        return float(m.group(1))

    return np.nan

def normalize_uygulama_suresi(val):
    """
    UygulamaSuresi'ni **dakika** cinsinden sayıya çevirir.
    Örnekler:
      - '20 Dakika' / '45 dk'     -> 20 / 45
      - '1 Saat' / '1.5 saat'     -> 60 / 90
      - '90 sn' / '90 saniye'     -> 1.5
      - '30' (birim yok)          -> 30 (dakika varsayılır)
    """
    if pd.isna(val):
        return np.nan
    s = str(val).lower().strip().replace(",", ".")
    m = re.search(r"(\d+(?:\.\d+)?)", s)
    if not m:
        return np.nan
    v = float(m.group(1))
    if "saat" in s:
        return v * 60.0
    if "sn" in s or "saniye" in s:
        return v / 60.0
    # 'dk' / 'dakika' / birim belirtilmemiş -> dakika
    return v

