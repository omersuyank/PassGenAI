import streamlit as st
import joblib
import os
import pandas as pd
import numpy as np
import string
from sklearn.preprocessing import LabelEncoder
import random

def password_to_numeric(password, max_length=16):
    char_mapping = {char: idx + 1 for idx, char in enumerate(string.ascii_letters + string.digits + "!@#$%^&*()-_=+<>?/")}
    numeric_representation = [char_mapping.get(char, 0) for char in password]

    if len(numeric_representation) < max_length:
        numeric_representation += [0] * (max_length - len(numeric_representation))
    else:
        numeric_representation = numeric_representation[:max_length]

    return numeric_representation

def suggest_stronger_password(password):
    new_password = list(password)

    if not any(c.islower() for c in password):
        new_password.append(random.choice(string.ascii_lowercase))

    if not any(c.isupper() for c in password):
        new_password.append(random.choice(string.ascii_uppercase))

    if not any(c.isdigit() for c in password):
        new_password.append(str(random.randint(0, 9)))

    special_chars = "!@#$%^&*()-_=+<>?/"
    if not any(c in special_chars for c in password):
        new_password.append(random.choice(special_chars))

    while len(new_password) < 12:
        new_password.append(random.choice(string.ascii_letters + string.digits + special_chars))

    random.shuffle(new_password)
    return ''.join(new_password)

st.set_page_config(page_title="PassGenAI Model Test Arayüzü", layout="centered")

st.title("🔐 PassGenAI: Şifre Güvenlik Modeli Test Arayüzü")
st.markdown("Eğitilmiş modelleri kullanarak şifre güvenlik seviyesini test edin!")

models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
model_files = [f for f in os.listdir(models_dir) if f.endswith(".pkl") and "SVM" not in f]

if not model_files:
    st.error("⚠ Henüz eğitilmiş model bulunamadı. Lütfen `train_models.py` dosyasını çalıştırarak modelleri eğitin.")
else:
    selected_model_file = st.selectbox("📌 Test etmek istediğiniz modeli seçin:", model_files)
    model_path = os.path.join(models_dir, selected_model_file)
    model = joblib.load(model_path)

    user_password = st.text_input("🔑 Şifrenizi girin:", type="default")

    def predict_security_level(password):
        password_features = np.array(password_to_numeric(password)).reshape(1, -1)
        prediction = model.predict(password_features)

        if isinstance(prediction[0], np.ndarray):
            predicted_value = int(round(prediction[0][0]))
        else:
            predicted_value = int(round(prediction[0]))

        security_mapping = {
            0: "Very Weak",
            1: "Weak",
            2: "Moderate",
            3: "Strong",
            4: "Very Strong"
        }

        return security_mapping.get(predicted_value, "Unknown")

    if user_password:
        predicted_level = predict_security_level(user_password)
        st.success(f"✅ Tahmini Güvenlik Seviyesi: **{predicted_level}**")

        if predicted_level in ["Very Weak", "Weak"]:
            suggested_password = suggest_stronger_password(user_password)
            st.warning(f"⚠ Şifreniz zayıf görünüyor. Önerilen güvenli şifre: **{suggested_password}**")

    st.markdown("---")
    st.markdown("🔹 **PassGenAI ile şifre güvenliğinizi artırın!**")
