import random
import string
import pandas as pd
import os


def generate_password(length=12):
    """En az bir büyük harf, küçük harf, rakam ve özel karakter içeren şifre üretir."""
    lower = random.choice(string.ascii_lowercase)
    upper = random.choice(string.ascii_uppercase)
    digit = random.choice(string.digits)
    special = random.choice("!@#$%^&*()_+-=[]{}|;:,.<>?/")

    remaining_length = length - 4
    all_chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?/"
    remaining_chars = ''.join(random.choices(all_chars, k=remaining_length))

    password = list(lower + upper + digit + special + remaining_chars)
    random.shuffle(password)
    return ''.join(password)


def assess_security(password):

    score = 0
    if any(c.islower() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?/" for c in password):
        score += 1
    if len(password) >= 12:
        score += 1

    security_levels = {1: "Very Weak", 2: "Weak", 3: "Moderate", 4: "Strong", 5: "Very Strong"}
    return security_levels.get(score, "Very Weak")


def create_password_dataset(size=1000000):

    data = []
    for _ in range(size):
        length = random.randint(8, 16)
        password = generate_password(length)
        security_level = assess_security(password)

        data.append({
            "Password": password,
            "Length": length,
            "Has_Uppercase": 1,
            "Has_Digits": 1,
            "Has_Special": 1,
            "Security_Level": security_level
        })

    df = pd.DataFrame(data)


    df = df.groupby("Security_Level", group_keys=False).apply(lambda x: x.sample(min(len(x), size // 5)))

    return df


# 'PassGenAI/data' klasörünü kontrol et ve yoksa oluştur
output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(output_dir, exist_ok=True)

# Veri setini oluştur ve kaydet
output_path = os.path.join(output_dir, "password_dataset.csv")
df = create_password_dataset()
df.to_csv(output_path, index=False)

print(f"Şifre veri seti oluşturuldu ve '{output_path}' dosyasına kaydedildi!")