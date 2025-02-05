import os
import time
import joblib
import pandas as pd
import numpy as np
import string
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder

input_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "password_dataset.csv")
df = pd.read_csv(input_path)

def password_to_numeric(password, max_length=16):
    char_mapping = {char: idx + 1 for idx, char in enumerate(string.ascii_letters + string.digits + "!@#$%^&*()-_=+<>?/")}
    numeric_representation = [char_mapping.get(char, 0) for char in password]

    if len(numeric_representation) < max_length:
        numeric_representation += [0] * (max_length - len(numeric_representation))
    else:
        numeric_representation = numeric_representation[:max_length]

    return numeric_representation

X = df["Weak_Password"].apply(password_to_numeric).tolist()
y_numeric = df["Strong_Password"].apply(password_to_numeric).tolist()

le = LabelEncoder()
y_labels = le.fit_transform(df["Strong_Password"])

X_train, X_test, y_train_numeric, y_test_numeric = train_test_split(X, y_numeric, test_size=0.2, random_state=42)
X_train, X_test, y_train_labels, y_test_labels = train_test_split(X, y_labels, test_size=0.2, random_state=42)

models = {
    "RandomForest": (RandomForestRegressor(n_estimators=10, max_depth=10, n_jobs=-1, random_state=42, verbose=1), y_train_numeric, y_test_numeric),
    "LinearRegression": (LinearRegression(), y_train_labels, y_test_labels),
    "SVM": (SVR(kernel='rbf'), y_train_labels, y_test_labels)
}

model_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
os.makedirs(model_dir, exist_ok=True)

for name, (model, y_train, y_test) in models.items():
    print(f"\n🔍 {name} modeli eğitiliyor...\n")

    start_time = time.time()
    epoch_times = []

    for epoch in tqdm(range(1, 6), desc=f"📈 {name} Eğitimi", unit="epoch"):
        epoch_start = time.time()
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        mse = mean_squared_error(y_test, predictions)
        epoch_time = time.time() - epoch_start
        epoch_times.append(epoch_time)

        avg_epoch_time = np.mean(epoch_times)
        remaining_time = avg_epoch_time * (5 - epoch)

        print(f"  🔹 {epoch}. Epoch")
        print(f"     🎯 Ortalama Hata (MSE): {mse:.4f}")
        print(f"     ⏳ Epoch süresi: {epoch_time:.2f} saniye")
        print(f"     ⏳ Tahmini kalan süre: {remaining_time:.2f} saniye\n")

    total_time = time.time() - start_time
    print(f"✅ {name} modeli eğitildi! Toplam süre: {total_time:.2f} saniye")

    model_path = os.path.join(model_dir, f"{name}.pkl")
    joblib.dump(model, model_path)
    print(f"💾 {name} modeli kaydedildi: {model_path}")
