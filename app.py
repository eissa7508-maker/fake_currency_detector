import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import streamlit as st
import cv2
import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim

# إعدادات واجهة الموقع
st.set_page_config(page_title="نظام كشف العملات المزورة", layout="centered")

st.title("🔍 مشروع التخرج: نظام فحص العملات")
st.write("قم برفع صورة العملة الأصلية وصورة العملة المراد فحصها للمقارنة")

# رفع الصور
col1, col2 = st.columns(2)
with col1:
    ref_file = st.file_uploader("ارفع العملة الأصلية (Reference)", type=['jpg', 'png', 'jpeg'])
with col2:
    test_file = st.file_uploader("ارفع العملة للفحص (Test)", type=['jpg', 'png', 'jpeg'])

if ref_file and test_file:
    # تحويل الملفات المرفوعة إلى صور OpenCV
    ref_image = Image.open(ref_file)
    test_image = Image.open(test_file)
    
    img1 = cv2.cvtColor(np.array(ref_image), cv2.COLOR_RGB2BGR)
    img2 = cv2.cvtColor(np.array(test_image), cv2.COLOR_RGB2BGR)

    # معالجة الصور (توحيد الحجم والتحويل للرمادي)
    img1_res = cv2.resize(img1, (600, 300))
    img2_res = cv2.resize(img2, (600, 300))
    
    gray1 = cv2.cvtColor(img1_res, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2_res, cv2.COLOR_BGR2GRAY)

    # تنفيذ خوارزمية المقارنة
    score, diff = ssim(gray1, gray2, full=True)

    # عرض النتائج
    st.divider()
    st.subheader(f"نتيجة التطابق: {score * 100:.2f}%")

    if score > 0.85:
        st.success("✅ النتيجة: العملة تبدو سليمة")
    else:
        st.error("🚨 النتيجة: تحذير! هناك اختلاف كبير، العملة قد تكون مزورة")

    # عرض صور الاختلافات
    diff = (diff * 255).astype("uint8")
    st.image(diff, caption="خريطة الاختلافات (المناطق المظلمة تعني اختلافاً)", use_column_width=True)