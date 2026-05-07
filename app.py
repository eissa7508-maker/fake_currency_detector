import os
import numpy as np
from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

app = Flask(__name__)

# 1. تحميل النموذج (تأكد من وضع ملف النموذج بجانب هذا الملف)
# استبدل 'model.h5' باسم ملف نموذجك الحقيقي
MODEL_PATH = 'model.h5' 
model = load_model(MODEL_PATH)

# 2. دالة معالجة الصورة قبل الفحص
def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224)) # تأكد من المقاس المناسب لنموذجك
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = x / 255.0 # تطبيع الصورة
    
    preds = model.predict(x)
    return preds

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        
        # حفظ الصورة مؤقتاً لفحصها
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 'uploads', f.filename)
        
        if not os.path.exists(os.path.join(basepath, 'uploads')):
            os.makedirs(os.path.join(basepath, 'uploads'))
            
        f.save(file_path)

        # تشغيل الفحص
        preds = model_predict(file_path, model)

        # تحويل النتيجة لنص (افترضنا أن 0 تعني مزورة و 1 سليمة)
        # عدل هذه الشروط حسب ترتيب الكلاسات في تدريبك
        if preds[0] > 0.5:
            result = "هذه العملة: سليمـة ✅"
        else:
            result = "تحذير: هذه العملة مزورة ❌"

        return render_template('index.html', prediction_text=result)
    return None

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)