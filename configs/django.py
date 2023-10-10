from pathlib import Path


# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Tencent 短信接口
SECRET_ID = ''
SECRET_KEY = ''
SMS_SDK_APP_ID = ''
TEMPLATE_ID = ''
SIGN_NAME = ''
REGION = ''

# 系统接口
# CRM_URL = None
CRM_URL = 'http://127.0.0.1:11901/api/admin/register_account/'
