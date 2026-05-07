import os
import numpy as np
from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

app = Flask(__name__)

# تحميل النموذج باسمه الصحيح الموجود في جهازك
MODEL_PATH = 'currency_model.h5'
model = load_model(MODEL_PATH)

# المسار الرئيسي لفتح الواجهة (هذا هو السطر الناقص عندك!)
@app.route('/')
def home():
    return render_template('index.html')

# مسار الفحص
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return "No file part", 400
    
    f = request.files['file']
    if f.filename == '':
        return "No selected file", 400

    # حفظ الصورة وفحصها
    basepath = os.path.dirname(__file__)
    file_path = os.path.join(basepath, 'uploads', f.filename)
    if not os.path.exists(os.path.join(basepath, 'uploads')):
        os.makedirs(os.path.join(basepath, 'uploads'))
    f.save(file_path)

    # معالجة الصورة للنموذج
    img = image.load_img(file_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = x / 255.0

    preds = model.predict(x)
    
    # تحديد النتيجة
    if preds[0] > 0.5:
        result = "هذه العملة: سليمـة ✅"
    else:
        result = "تحذير: هذه العملة مزورة ❌"

    return render_template('index.html', prediction_text=result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)