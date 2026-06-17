
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

df = pd.read_csv("data/simulated_campaign_data.csv")
df["converted_flag"] = (df["conversions"] > 0).astype(int)

features = [
    "impressions", "clicks", "cost", "ctr", "cpc", "customer_quality_score",
    "channel", "keyword", "device", "geography", "audience_segment"
]
X = df[features]
y = df["converted_flag"]

num_cols = ["impressions", "clicks", "cost", "ctr", "cpc", "customer_quality_score"]
cat_cols = ["channel", "keyword", "device", "geography", "audience_segment"]

preprocess = ColumnTransformer([
    ("num", StandardScaler(), num_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols)
])

model = Pipeline([
    ("preprocess", preprocess),
    ("rf", RandomForestClassifier(n_estimators=150, random_state=42, class_weight="balanced"))
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
model.fit(X_train, y_train)
pred = model.predict(X_test)
proba = model.predict_proba(X_test)[:, 1]

Path("reports").mkdir(exist_ok=True)
metrics_text = []
metrics_text.append("# Conversion Prediction Model Report\n")
metrics_text.append("## Model")
metrics_text.append("Random Forest classifier predicting whether a campaign row generated conversions.\n")
metrics_text.append("## ROC-AUC")
metrics_text.append(f"{roc_auc_score(y_test, proba):.3f}\n")
metrics_text.append("## Classification Report")
metrics_text.append(classification_report(y_test, pred))

Path("reports/model_report.txt").write_text("\n".join(metrics_text))

# KMeans segmentation
cluster_df = df.groupby(["campaign", "channel", "audience_segment"]).agg({
    "impressions": "sum",
    "clicks": "sum",
    "cost": "sum",
    "conversions": "sum",
    "revenue": "sum",
    "customer_quality_score": "mean"
}).reset_index()

cluster_df["ctr"] = cluster_df["clicks"] / cluster_df["impressions"]
cluster_df["cpa"] = cluster_df["cost"] / cluster_df["conversions"].replace(0, np.nan)
cluster_df["roas"] = cluster_df["revenue"] / cluster_df["cost"].replace(0, np.nan)
cluster_df = cluster_df.replace([np.inf, -np.inf], np.nan).fillna(0)

cluster_features = ["ctr", "cpa", "roas", "customer_quality_score", "cost", "conversions"]
scaler = StandardScaler()
Z = scaler.fit_transform(cluster_df[cluster_features])
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
cluster_df["cluster"] = kmeans.fit_predict(Z)

# Label clusters by simple business logic
cluster_summary = cluster_df.groupby("cluster")[cluster_features].mean().reset_index()
cluster_summary.to_csv("reports/cluster_summary.csv", index=False)
cluster_df.to_csv("reports/campaign_clusters.csv", index=False)

print("Created ML model report and campaign clusters.")
