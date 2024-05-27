from pathlib import Path

import environ

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR / ".env"))

DEBUG = env.bool("DJANGO_DEBUG", False)

TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = [str(ROOT_DIR / "locale")]

DATABASES = {
    'default': {
        'ENGINE' : 'django.db.backends.postgresql',
        'HOST' : os.environ.get('DB_HOST'),
        'NAME' : os.environ.get('DB_NAME'),
        'USER' : os.environ.get('DB_USER'),
        'PASSWORD' : os.environ.get('DB_PASS'),
    }
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ROOT_URLCONF = "app.urls"

WSGI_APPLICATION = "app.wsgi.application"

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'corsheaders',
    'drf_spectacular',
    'debug_toolbar'
]

LOCAL_APPS = [
    'user',
    'core',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]
