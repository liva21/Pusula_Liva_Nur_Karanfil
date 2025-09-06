from typing import List, Dict, Tuple
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

def build_multilabel_matrix(df: pd.DataFrame, mlb_fields: List[str], top_k: int = 25) -> Tuple[pd.DataFrame, Dict[str, List[str]]]:
    frames = []; vocab = {}
    for col in mlb_fields:
        if f"{col}__list" not in df.columns: continue
        lists = df[f"{col}__list"]; freq = {}
        for lst in lists:
            for t in lst: freq[t] = freq.get(t, 0) + 1
        top = sorted(freq, key=freq.get, reverse=True)[:top_k]; vocab[col] = top
        bin_df = pd.DataFrame(0, index=df.index, columns=[f"{col}__{t}" for t in top], dtype=int)
        for i, lst in enumerate(lists):
            for t in lst:
                if t in top: bin_df.at[i, f"{col}__{t}"] = 1
        frames.append(bin_df)
    X_mlb = pd.concat(frames, axis=1) if frames else pd.DataFrame(index=df.index)
    return X_mlb, vocab

def build_preprocessor(num_features: List[str], cat_features: List[str]) -> ColumnTransformer:
    numeric = Pipeline([("imp", SimpleImputer(strategy="median")), ("scaler", StandardScaler())])
    categorical = Pipeline([("imp", SimpleImputer(strategy="most_frequent")),
                            ("ohe", OneHotEncoder(handle_unknown="ignore", sparse_output=False))])
    return ColumnTransformer([("num", numeric, num_features), ("cat", categorical, cat_features)], remainder="drop")

def transform_features(df: pd.DataFrame, num_features: List[str], cat_features: List[str], mlb_fields: List[str], top_k: int = 25):
    pre = build_preprocessor(num_features, cat_features)
    X_base = pre.fit_transform(df)
    ohe_names = pre.named_transformers_["cat"].named_steps["ohe"].get_feature_names_out(cat_features).tolist() if cat_features else []
    import pandas as pd
    X_base_df = pd.DataFrame(X_base, columns=list(num_features)+ohe_names, index=df.index)
    X_mlb, vocab = build_multilabel_matrix(df, mlb_fields, top_k=top_k)
    X_full = pd.concat([X_base_df, X_mlb], axis=1)
    return X_full, vocab, pre
