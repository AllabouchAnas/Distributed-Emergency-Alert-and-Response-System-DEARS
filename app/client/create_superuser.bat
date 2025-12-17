@echo off
echo Creating Django superuser for DEARS...
echo.
echo Please enter the following details:
echo Username: admin
echo Email: admin@dears.local
echo Password: (you choose)
echo.
python manage.py createsuperuser --username admin --email admin@dears.local
