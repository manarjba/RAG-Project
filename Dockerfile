FROM python:3.11-slim

# إعداد مجلد العمل داخل الحاوية
WORKDIR /app

# نسخ ملفات المشروع بالكامل
COPY . .

# إعداد المسار حتى يتعرف بايثون على مجلد app كموديول
ENV PYTHONPATH="${PYTHONPATH}:/app"

# تثبيت المتطلبات
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app/main.py"]
