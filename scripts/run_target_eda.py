#!/usr/bin/env python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.preprocessing.cleaning import standardize_text_columns, normalize_tedavi_suresi

TARGET = "TedaviSuresi"

def save_scatter(x, y, x_name, outdir):
    fig = plt.figure()
    plt.scatter(x, y, alpha=0.5)
    plt.xlabel(x_name); plt.ylabel(TARGET); plt.title(f"{x_name} vs {TARGET}")
    out = Path(outdir) / f"scatter_{x_name}_vs_{TARGET}.png"
    plt.tight_layout(); fig.savefig(out, dpi=150); plt.close(fig)

def save_box(df, cat_col, y_col, outdir, topn=10, min_count=20):
    counts = df[cat_col].value_counts().head(topn).index
    sub = df[df[cat_col].isin(counts)].copy()
    grp_counts = sub[cat_col].value_counts()
    keep = grp_counts[grp_counts >= min_count].index
    sub = sub[sub[cat_col].isin(keep)]
    if sub.empty:
        return
    order = sub.groupby(cat_col)[y_col].median().sort_values(ascending=False).index
    fig = plt.figure(figsize=(8, max(3, len(order)*0.4)))
    sub[cat_col] = pd.Categorical(sub[cat_col], categories=order, ordered=True)
    sub.boxplot(column=y_col, by=cat_col, vert=False)
    plt.title(f"{y_col} by {cat_col}"); plt.suptitle("")
    plt.xlabel(y_col); plt.ylabel(cat_col)
    out = Path(outdir) / f"box_{y_col}_by_{cat_col}.png"
    plt.tight_layout(); fig.savefig(out, dpi=150); plt.close(fig)

def main(excel, outdir="outputs/figures_target"):
    outdir = Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
    df = pd.read_excel(excel)
    df = standardize_text_columns(df)
    df[TARGET] = df[TARGET].apply(normalize_tedavi_suresi)
    df[TARGET] = pd.to_numeric(df[TARGET], errors="coerce")

    # scatter: numerik -> hedef
    for col in ["Yas", "UygulamaSuresi"]:
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            mask = df[col].notna() & df[TARGET].notna()
            if mask.any():
                save_scatter(df.loc[mask, col], df.loc[mask, TARGET], col, outdir)

    # box: kategorik -> hedef
    for col in ["Bolum","Cinsiyet","KanGrubu","Uyruk","TedaviAdi"]:
        if col in df.columns:
            save_box(df[[col, TARGET]].dropna(), col, TARGET, outdir, topn=10)

    print(f"Saved figures to {outdir}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--excel", required=True)
    ap.add_argument("--outdir", default="outputs/figures_target")
    args = ap.parse_args()
    main(args.excel, args.outdir)

