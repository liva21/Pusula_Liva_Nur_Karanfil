import pandas as pd, matplotlib.pyplot as plt
from pathlib import Path

def hist(series: pd.Series, title: str, outdir: Path):
    fig = plt.figure(); plt.hist(series.dropna(), bins=30)
    plt.title(title); plt.xlabel(title); plt.ylabel("Frequency")
    out = outdir / f"{title.replace(' ','_')}.png"; plt.tight_layout(); fig.savefig(out, dpi=150); plt.close(fig); return out

def bar_top_counts(series: pd.Series, title: str, outdir: Path, topn: int = 20):
    counts = series.astype(str).str.strip().value_counts().head(topn)
    fig = plt.figure(figsize=(8, max(3, len(counts)*0.3))); counts[::-1].plot(kind="barh")
    plt.title(title); plt.xlabel("Count")
    out = outdir / f"{title.replace(' ','_')}_top{topn}.png"; plt.tight_layout(); fig.savefig(out, dpi=150); plt.close(fig); return out

def corr_heatmap(df: pd.DataFrame, numeric_cols, outdir: Path, title="Correlation_Heatmap"):
    if len(numeric_cols) < 2: return None
    corr = df[numeric_cols].corr(numeric_only=True)
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(6,5)); plt.imshow(corr, interpolation="nearest")
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=90); plt.yticks(range(len(corr.index)), corr.index)
    plt.colorbar(); plt.title(title); out = outdir / f"{title}.png"; plt.tight_layout(); fig.savefig(out, dpi=150); plt.close(fig); return out
