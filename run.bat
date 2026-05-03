@echo off
echo Mengatur database...
python manage.py makemigrations
python manage.py migrate

echo.
echo Membuat superuser admin (user: admin, pass: admin)...
set DJANGO_SUPERUSER_PASSWORD=admin
python manage.py createsuperuser --username admin --email admin@example.com --noinput 2>nul
if %errorlevel% neq 0 (
    echo Superuser mungkin sudah ada.
)

echo.
echo Menjalankan server kasir...
python manage.py runserver 0.0.0.0:8000
