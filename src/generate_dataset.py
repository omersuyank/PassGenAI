import random
import string
import pandas as pd
import os


# 📌 Şifre oluşturma fonksiyonları
def generate_very_weak_password():
    """Çok zayıf (Very Weak) şifreler oluşturur."""
    common_passwords = ["123456", "password", "admin", "qwerty", "111111", "abc123", "letmein", "123123", "passw0rd"]
    return random.choice(common_passwords)


def generate_weak_password():
    """Zayıf (Weak) şifreler oluşturur."""
    base_words = ["hello", "welcome", "sunshine", "chocolate", "dragon", "football", "monkey"]
    return random.choice(base_words) + str(random.randint(100, 999))


def generate_moderate_password():
    """Orta seviye (Moderate) şifreler oluşturur."""
    base = random.choice(["Python", "Security", "Network", "Laptop", "Gaming"])
    return base + random.choice("!@#$%^&*") + str(random.randint(1000, 9999))


def generate_strong_password():
    """Güçlü (Strong) şifreler oluşturur."""
    base = ''.join(random.choices(string.ascii_letters, k=6))
    return base + random.choice("!@#$%^&*") + str(random.randint(1000, 9999))


def generate_very_strong_password(length=14):
    """Çok güçlü (Very Strong) rastgele şifreler oluşturur."""
    all_chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+<>?/"

    return ''.join(random.choices(all_chars, k=length))


def generate_stronger_version(weak_password):
    """Zayıf bir şifreyi daha güçlü bir hale getirir."""

    new_password = list(weak_password)

    # 🔹 Küçük harf yoksa ekleyelim
    if not any(c.islower() for c in weak_password):
        new_password.append(random.choice(string.ascii_lowercase))

    # 🔹 Büyük harf yoksa ekleyelim
    if not any(c.isupper() for c in weak_password):
        new_password.append(random.choice(string.ascii_uppercase))

    # 🔹 Rakam yoksa ekleyelim
    if not any(c.isdigit() for c in weak_password):
        new_password.append(str(random.randint(0, 9)))

    # 🔹 Özel karakter yoksa ekleyelim
    special_chars = "!@#$%^&*()-_=+<>?/"
    if not any(c in special_chars for c in weak_password):
        new_password.append(random.choice(special_chars))

    # 🔹 Uzunluğu en az 12 karakter olacak şekilde ayarlayalım
    while len(new_password) < 12:
        new_password.append(random.choice(string.ascii_letters + string.digits + special_chars))

    # 🔹 Şifreyi biraz karıştır ama temel yapısını koru
    random.shuffle(new_password)

    return ''.join(new_password)


# 📌 Veri setini oluştur
size_per_category = 200000  # Her güvenlik seviyesi için 200.000 örnek
data = []

for _ in range(size_per_category):
    weak_pw = generate_very_weak_password()
    strong_pw = generate_stronger_version(weak_pw)
    data.append({"Weak_Password": weak_pw, "Strong_Password": strong_pw, "Security_Level": "Very Weak"})

    weak_pw = generate_weak_password()
    strong_pw = generate_stronger_version(weak_pw)
    data.append({"Weak_Password": weak_pw, "Strong_Password": strong_pw, "Security_Level": "Weak"})

    weak_pw = generate_moderate_password()
    strong_pw = generate_stronger_version(weak_pw)
    data.append({"Weak_Password": weak_pw, "Strong_Password": strong_pw, "Security_Level": "Moderate"})

    strong_pw = generate_strong_password()
    data.append({"Weak_Password": strong_pw, "Strong_Password": strong_pw, "Security_Level": "Strong"})

    strong_pw = generate_very_strong_password()
    data.append({"Weak_Password": strong_pw, "Strong_Password": strong_pw, "Security_Level": "Very Strong"})

# 📌 DataFrame oluştur
df = pd.DataFrame(data)

# 📌 Şifre uzunluğu ve karakteristik özelliklerini ekleyelim
df["Weak_Length"] = df["Weak_Password"].apply(len)
df["Strong_Length"] = df["Strong_Password"].apply(len)
df["Weak_Has_Uppercase"] = df["Weak_Password"].apply(lambda x: int(any(c.isupper() for c in x)))
df["Weak_Has_Digits"] = df["Weak_Password"].apply(lambda x: int(any(c.isdigit() for c in x)))
df["Weak_Has_Special"] = df["Weak_Password"].apply(lambda x: int(any(c in "!@#$%^&*()-_=+<>?/" for c in x)))

df["Strong_Has_Uppercase"] = df["Strong_Password"].apply(lambda x: int(any(c.isupper() for c in x)))
df["Strong_Has_Digits"] = df["Strong_Password"].apply(lambda x: int(any(c.isdigit() for c in x)))
df["Strong_Has_Special"] = df["Strong_Password"].apply(lambda x: int(any(c in "!@#$%^&*()-_=+<>?/" for c in x)))

# 📌 Dosya yolunu ayarla ve kaydet
output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "password_dataset.csv")
df.to_csv(output_path, index=False)

print(f"✅ Yeni şifre dönüşüm veri seti oluşturuldu ve '{output_path}' dosyasına kaydedildi!")
