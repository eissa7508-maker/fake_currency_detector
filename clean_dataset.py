import os
from PIL import Image

base = "currency_dataset"

bad_files = []

for root, dirs, files in os.walk(base):
    for file in files:
        path = os.path.join(root, file)
        try:
            img = Image.open(path)
            img.verify()  # يتأكد إنها صورة حقيقية
        except:
            bad_files.append(path)

# حذف الملفات التالفة
for f in bad_files:
    print("Deleting:", f)
    os.remove(f)

print("Done cleaning. Removed:", len(bad_files))