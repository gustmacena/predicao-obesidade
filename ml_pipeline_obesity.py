# -*- coding: utf-8 -*-
import pandas as pd, numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from packaging import version
import sklearn, joblib

# =========================================================
# 1) Leitura
# =========================================================
CSV_PATH = Path("Obesity.csv")  # garanta que está na mesma pasta
df = pd.read_csv(CSV_PATH)

# =========================================================
# 2) Renomear colunas (PT-BR)
# =========================================================
col_map_pt = {
    "Gender": "Gênero",
    "Age": "Idade",
    "Height": "Altura",
    "Weight": "Peso",
    "family_history": "Histórico Familiar",
    "FAVC": "FAVC",
    "FCVC": "FCVC",
    "NCP": "NCP",
    "CAEC": "CAEC",
    "SMOKE": "Fuma",
    "CH2O": "Água por dia",
    "SCC": "Conta Calorias",
    "FAF": "Atividade Física",
    "TUE": "Tempo em Telas",
    "CALC": "Álcool",
    "MTRANS": "Transporte",
    "Obesity": "Obesidade"
}
df = df.rename(columns=col_map_pt)

# =========================================================
# 3) Mapear categorias para PT-BR (features)
# =========================================================
def map_vals(col, mapping):
    if col in df.columns:
        df[col] = df[col].map(mapping).fillna(df[col])

map_vals("Gênero", {"Male": "Masculino", "Female": "Feminino"})
map_vals("Histórico Familiar", {"yes": "Sim", "no": "Não"})
map_vals("FAVC", {"yes": "Sim", "no": "Não"})
map_vals("Fuma", {"yes": "Sim", "no": "Não"})
map_vals("Conta Calorias", {"yes": "Sim", "no": "Não"})
map_vals("CAEC", {"Sometimes": "Às vezes", "Frequently": "Frequentemente", "Always": "Sempre", "no": "Não"})
map_vals("Álcool", {"no": "Não", "Sometimes": "Às vezes", "Frequently": "Frequentemente", "Always": "Sempre"})
map_vals("Transporte", {
    "Public_Transportation": "Transporte público",
    "Walking": "Caminhada",
    "Automobile": "Automóvel",
    "Motorbike": "Motocicleta",
    "Bike": "Bicicleta"
})

# =========================================================
# 4) Target e features (em PT-BR) + tradução das CLASSES do alvo
# =========================================================
target_col = "Obesidade"

# Traduz as classes do alvo para PT-BR
target_map_pt = {
    "Insufficient_Weight": "Baixo_peso",
    "Normal_Weight": "Peso_normal",
    "Overweight_Level_I": "Sobrepeso_I",
    "Overweight_Level_II": "Sobrepeso_II",
    "Obesity_Type_I": "Obesidade_I",
    "Obesity_Type_II": "Obesidade_II",
    "Obesity_Type_III": "Obesidade_III",
}
y = df[target_col].map(target_map_pt).astype("category")

X = df.drop(columns=[target_col])

# Garante tipos numéricos corretos (evita problemas de vírgula/locale)
num_cols = X.select_dtypes(include=[np.number]).columns.tolist()
for c in ["Idade", "Altura", "Peso", "FCVC", "NCP", "Água por dia", "Atividade Física", "Tempo em Telas"]:
    if c in X.columns:
        X[c] = pd.to_numeric(X[c], errors="coerce")

cat_cols = X.select_dtypes(include=["object"]).columns.tolist()
num_cols = X.select_dtypes(include=[np.number]).columns.tolist()

# =========================================================
# 5) Pré-processamento (compatível com várias versões do sklearn)
# =========================================================
from sklearn.preprocessing import OneHotEncoder
ohe_kwargs = {"handle_unknown": "ignore"}
if version.parse(sklearn.__version__) >= version.parse("1.2"):
    ohe_kwargs["sparse_output"] = False
else:
    ohe_kwargs["sparse"] = False
ohe = OneHotEncoder(**ohe_kwargs)

preprocess = ColumnTransformer([
    ("num", StandardScaler(), num_cols),
    ("cat", ohe, cat_cols)
])

pipe = Pipeline([("prep", preprocess), ("clf", GradientBoostingClassifier(random_state=42))])

# =========================================================
# 6) Validação (CV) + Holdout
# =========================================================
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(pipe, X, y, cv=cv, scoring="accuracy")
print("CV mean acc:", scores.mean(), "folds:", scores)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
pipe.fit(X_train, y_train)
y_pred = pipe.predict(X_test)
print("Holdout acc:", accuracy_score(y_test, y_pred))
print("Report:\n", classification_report(y_test, y_pred, zero_division=0))
print("CM:\n", confusion_matrix(y_test, y_pred))

# =========================================================
# 7) Exporta modelo PT-BR
# =========================================================
MODEL_PATH = Path("obesity_pipeline.pkl")
pipe.fit(X, y)
joblib.dump(pipe, MODEL_PATH)
print("Modelo PT salvo em", MODEL_PATH.resolve())
