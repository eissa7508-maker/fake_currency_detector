import os
import numpy as np
from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

app = Flask(__name__)

# تحميل النموذج
MODEL_PATH = 'currency_model.h5'
model = load_model(MODEL_PATH)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return "No file part", 400
    
    f = request.files['file']
    if f.filename == '':
        return "No selected file", 400

    # حفظ الصورة في مجلد مؤقت (Hugging Face يسمح بالكتابة في /tmp أو المجلد الحالي)
    basepath = os.path.dirname(__file__)
    upload_path = os.path.join(basepath, 'uploads')
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
        
    file_path = os.path.join(upload_path, f.filename)
    f.save(file_path)

    # معالجة الصورة
    img = image.load_img(file_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = x / 255.0

    preds = model.predict(x)
    
    if preds[0] > 0.5:
        result = "هذه العملة: سليمـة ✅"
    else:
        result = "تحذير: هذه العملة مزورة ❌"

    return render_template('index.html', prediction_text=result)

# التعديل المهم جداً لـ Hugging Face هنا:
if __name__ == '__main__':
    # Hugging Face بيستخدم بورت 7860 افتراضياً
    app.run(host='0.0.0.0', port=7860)
