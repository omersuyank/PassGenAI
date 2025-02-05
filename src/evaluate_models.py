import os
import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder

# Veri setini yükle
data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "password_dataset.csv")
df = pd.read_csv(data_path)

# Özellikleri ve hedef değişkeni ayır
X = df[['Length', 'Has_Uppercase', 'Has_Digits', 'Has_Special']]
y = df['Security_Level']

# Kategorik veriyi sayısala çevirme (Aynı LabelEncoder'ı kullanmalıyız)
le = LabelEncoder()
y = le.fit_transform(y)

# 'PassGenAI/models' klasöründeki tüm modelleri yükle
models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
models = {}

for model_file in os.listdir(models_dir):
    if model_file.endswith(".pkl"):
        model_path = os.path.join(models_dir, model_file)
        model_name = model_file.replace(".pkl", "")

        # joblib kullanarak modeli yükle
        models[model_name] = joblib.load(model_path)

# Her modelin doğruluğunu hesapla
for model_name, model in models.items():
    print(f"🔍 {model_name} modeli test ediliyor...")

    # Tahmin yap
    try:
        y_pred = model.predict(X)
        accuracy = accuracy_score(y, y_pred)
        print(f"✅ {model_name} Doğruluk: {accuracy:.4f}")
        print(classification_report(y, y_pred))
    except Exception as e:
        print(f"⚠ {model_name} test edilemedi: {e}")

print("✅ Tüm modeller test edildi ve sonuçlar karşılaştırıldı!")
