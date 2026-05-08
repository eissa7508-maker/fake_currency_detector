FROM python:3.9

# إعداد مجلد العمل
WORKDIR /code

# نسخ ملف المكتبات وتثبيتها
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# نسخ كل ملفات المشروع إلى السيرفر
COPY . .

# أمر تشغيل التطبيق (تأكد أن ملفك الأساسي اسمه app.py)
CMD ["python", "app.py"]
