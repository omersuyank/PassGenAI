import random
import string
import pandas as pd
import os

def generate_password(length=12, use_upper=True, use_digits=True, use_special=True):
    """Belirtilen kurallara göre rastgele şifre üretir."""
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase if use_upper else ""
    digits = string.digits if use_digits else ""
    special = "!@#$%^&*()_+-=[]{}|;:,.<>?/" if use_special else ""

    all_chars = lower + upper + digits + special
    return ''.join(random.choices(all_chars, k=length))

def create_password_dataset(size=20000):
    """Belirtilen sayıda rastgele şifre içeren bir veri seti oluşturur."""
    data = []
    for _ in range(size):
        length = random.randint(8, 24)  # Şifre uzunluğu 8-24 karakter arasında rastgele seçilir
        use_upper = random.choice([True, False])
        use_digits = random.choice([True, False])
        use_special = random.choice([True, False])

        password = generate_password(length, use_upper, use_digits, use_special)

        data.append({
            "Password": password,
            "Length": length,
            "Has_Uppercase": int(use_upper),
            "Has_Digits": int(use_digits),
            "Has_Special": int(use_special)
        })

    return pd.DataFrame(data)

# 'PassGenAI/data' klasörünü kontrol et ve yoksa oluştur
output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(output_dir, exist_ok=True)

# Veri setini oluştur ve kaydet
output_path = os.path.join(output_dir, "password_dataset.csv")
df = create_password_dataset()
df.to_csv(output_path, index=False)

print(f"Şifre veri seti oluşturuldu ve '{output_path}' dosyasına kaydedildi!")
