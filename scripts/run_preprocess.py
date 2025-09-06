
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import argparse
from pathlib import Path
import pandas as pd

from src.preprocessing.cleaning import (
    standardize_text_columns,
    winsorize_series,
    normalize_tedavi_suresi,
    normalize_uygulama_suresi,  
)
from src.preprocessing.build_features import transform_features

TARGET = "TedaviSuresi"

def pick_sheet_with_target(xls: pd.ExcelFile, target: str) -> str:
    for s in xls.sheet_names:
        tmp = pd.read_excel(xls, sheet_name=s)
        if target in tmp.columns:
            return s
    return xls.sheet_names[0]

def main(excel_path: str, outdir: str = "./outputs"):
    excel_path = Path(excel_path)
    outdir = Path(outdir); outdir.mkdir(parents=True, exist_ok=True)

  
    xls = pd.ExcelFile(excel_path)
    sheet = pick_sheet_with_target(xls, TARGET)
    df = pd.read_excel(xls, sheet_name=sheet)

  
    df = standardize_text_columns(df)

    
    if "UygulamaSuresi" in df.columns:
        df["UygulamaSuresi_min"] = df["UygulamaSuresi"].apply(normalize_uygulama_suresi)

   
    num_features = [c for c in ["Yas", "UygulamaSuresi_min"]
                    if c in df.columns and pd.api.types.is_numeric_dtype(df[c])]
    cat_features = [c for c in ["Cinsiyet", "KanGrubu", "Uyruk", "Bolum", "TedaviAdi"]
                    if c in df.columns]
    mlb_fields   = [c for c in ["KronikHastalik", "Alerji", "Tanilar", "UygulamaYerleri"]
                    if c in df.columns]

    
    X_full, ml_vocab, preproc = transform_features(
        df, num_features, cat_features, mlb_fields, top_k=25
    )

   
    y = None
    if TARGET in df.columns:
        y = pd.to_numeric(df[TARGET].apply(normalize_tedavi_suresi), errors="coerce")
        yw = winsorize_series(y)

    X_full.to_csv(outdir / "X_processed.csv", index=False)
    try:
        X_full.to_parquet(outdir / "X_processed.parquet", index=False)
    except Exception as e:
        print("Parquet save failed (install pyarrow). CSV saved. Err:", e)

    if y is not None:
        y.to_csv(outdir / "y_TedaviSuresi.csv", index=False)
        try:
            y.to_frame("TedaviSuresi").to_parquet(outdir / "y_TedaviSuresi.parquet", index=False)
        except Exception:
            pass
        yw.to_csv(outdir / "y_TedaviSuresi_winsorized.csv", index=False)
        try:
            yw.to_frame("TedaviSuresi_wins").to_parquet(outdir / "y_TedaviSuresi_winsorized.parquet", index=False)
        except Exception:
            pass

    
    meta = {
        "sheet": sheet,
        "num_features": num_features,
        "cat_features": cat_features,
        "mlb_fields": mlb_fields,
        "ml_vocab_sample": {k: v[:10] for k, v in ml_vocab.items()},
    }
    (outdir / "preprocess_meta.json").write_text(
        __import__("json").dumps(meta, indent=2), encoding="utf-8"
    )

    print("Preprocessing complete. Files in ./outputs")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--excel", required=True, help="Path to the Excel file")
    ap.add_argument("--outdir", default="./outputs")
    args = ap.parse_args()
    main(args.excel, args.outdir)

