import os
from flask import Flask, render_template, request, jsonify
# إخفاء تنبيهات تنسرفلو المزعجة
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

app = Flask(__name__)

# --- المسار الرئيسي (يفتح واجهة الموقع) ---
@app.route('/')
def home():
    return render_template('index.html')

# --- مسار فحص العملة (يستقبل الصورة ويعطي النتيجة) ---
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return "لم يتم رفع أي صورة", 400
    
    file = request.files['file']
    
    if file.filename == '':
        return "اسم الملف فارغ", 400

    if file:
        # هنا سيتم وضع كود تشغيل النموذج الخاص بك مستقبلاً
        # حالياً سنقوم بإرجاع رسالة تجريبية للتأكد من نجاح الربط
        return render_template('index.html', prediction_text="جاري فحص العملة... (هنا ستظهر النتيجة لاحقاً)")

if __name__ == '__main__':
    # تأكد من استخدام المنفذ 5000 أو المنفذ الذي يحدده Render تلقائياً
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)