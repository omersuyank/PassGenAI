import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# Veri seti yükleme
input_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "password_dataset.csv")
df = pd.read_csv(input_path)

# Gerekli sütunları seçme ve kategorik veriyi sayısala çevirme
X = df[["Length", "Has_Uppercase", "Has_Digits", "Has_Special"]]
y = df["Security_Level"]
le = LabelEncoder()
y = le.fit_transform(y)

# Veriyi eğitim ve test setlerine ayırma
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modelleri tanımlama
models = {
    "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42),
    "LogisticRegression": LogisticRegression(max_iter=1000),
    "SVM": SVC(kernel='linear', probability=True)
}

# Modelleri eğitme ve kaydetme
model_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
os.makedirs(model_dir, exist_ok=True)

for name, model in models.items():
    print(f"{name} model eğitiliyor...")
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"{name} doğruluk: {accuracy:.4f}")

    # Modeli kaydetme
    model_path = os.path.join(model_dir, f"{name}.pkl")
    joblib.dump(model, model_path)
    print(f"{name} modeli kaydedildi: {model_path}")
