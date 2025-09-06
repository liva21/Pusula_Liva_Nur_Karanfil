#!/usr/bin/env python
import argparse
from pathlib import Path
import pandas as pd, numpy as np
from src.preprocessing.cleaning import standardize_text_columns
from src.eda.plots import hist, bar_top_counts, corr_heatmap

TARGET = "TedaviSuresi"

def pick_sheet_with_target(xls: pd.ExcelFile, target: str) -> str:
    for s in xls.sheet_names:
        if target in pd.read_excel(xls, sheet_name=s).columns: return s
    return xls.sheet_names[0]

def main(excel_path: str, outdir: str = "./outputs", reportdir: str = "./reports"):
    excel_path = Path(excel_path)
    outdir, figdir, reportdir = Path(outdir), Path(outdir)/"figures", Path(reportdir)
    outdir.mkdir(parents=True, exist_ok=True); figdir.mkdir(parents=True, exist_ok=True); reportdir.mkdir(parents=True, exist_ok=True)

    xls = pd.ExcelFile(excel_path); sheet = pick_sheet_with_target(xls, TARGET)
    df = pd.read_excel(xls, sheet_name=sheet)

    df_clean = standardize_text_columns(df.copy())
    (outdir/"dtypes.csv").write_text(df.dtypes.astype(str).to_csv(), encoding="utf-8")
    miss = (df_clean.isna().sum()/len(df_clean)*100).round(2).rename("missing_%").to_frame(); miss.to_csv(outdir/"missing_percent.csv")
    num_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()
    if num_cols: df_clean[num_cols].describe().T.to_csv(outdir/"numeric_describe.csv")

    if "Yas" in df_clean: hist(df_clean["Yas"], "Histogram_Yas", figdir)
    if "UygulamaSuresi" in df_clean: hist(df_clean["UygulamaSuresi"], "Histogram_UygulamaSuresi", figdir)
    if TARGET in df_clean: hist(pd.to_numeric(df_clean[TARGET], errors="coerce"), "Histogram_TedaviSuresi", figdir)
    for col in ["Cinsiyet","KanGrubu","Uyruk","Bolum","TedaviAdi"]:
        if col in df_clean: bar_top_counts(df_clean[col], f"Top_{col}", figdir, topn=20)
    if len(num_cols) >= 2: corr_heatmap(df_clean, num_cols, figdir)

    (outdir/"shape.txt").write_text(f"Sheet: {sheet} | Shape: {df.shape[0]}x{df.shape[1]}\n", encoding="utf-8")
    (reportdir/"EDA_Summary_basic.md").write_text("\n".join([
        "# EDA Summary", f"- Sheet: {sheet}", f"- Shape: {df.shape[0]} x {df.shape[1]}",
        f"- Numeric columns: {num_cols}", "- Missingness: outputs/missing_percent.csv",
        "- Figures: outputs/figures/"
    ]), encoding="utf-8")
    print("EDA complete. See outputs/ and reports/")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--excel", required=True)
    ap.add_argument("--outdir", default="./outputs")
    ap.add_argument("--reportdir", default="./reports")
    args = ap.parse_args(); main(args.excel, args.outdir, args.reportdir)
