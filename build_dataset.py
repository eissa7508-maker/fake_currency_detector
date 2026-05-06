import os
import requests

base = "currency_dataset"
classes = ["usd", "eur", "sdg"]

# صور جاهزة (روابط عامة من Wikimedia)
images = {
    "usd": [
        "https://upload.wikimedia.org/wikipedia/commons/4/4c/United_States_one_dollar_bill%2C_obverse.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/2/2e/US_%24100_series_2009_Obverse.jpg"
    ],
    "eur": [
        "https://upload.wikimedia.org/wikipedia/commons/8/8f/Euro_Series_Banknotes.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/6/65/Euro_banknotes_%282019%29.jpg"
    ],
    "sdg": [
        "https://upload.wikimedia.org/wikipedia/commons/2/2e/Sudanese_pound_banknotes.jpg"
    ]
}

# إنشاء المجلدات
for c in classes:
    os.makedirs(f"{base}/{c}", exist_ok=True)

# تحميل الصور
for cls, urls in images.items():
    for i, url in enumerate(urls):
        try:
            img = requests.get(url).content
            path = f"{base}/{cls}/{cls}_{i}.jpg"
            with open(path, "wb") as f:
                f.write(img)
            print("Downloaded:", path)
        except:
            print("Failed:", url)

print("Dataset Ready 🚀")