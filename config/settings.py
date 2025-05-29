import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-!8==@fr40w4j1g=0(i!rn!qwtxp2lewg5$lwjr-gsz#069kfrg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps propias
    'usuarios',

    # Apps de terceros
    'crispy_forms',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', # Necesario para las sesiones
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Necesario para la autenticación
    'django.contrib.messages.middleware.MessageMiddleware', # Necesario para los mensajes
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # ... otros middlewares que puedas tener ...
]
CRISPY_TEMPLATE_PACK = 'bootstrap5'

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bolsa_trabajo',
        'USER': 'bolsa_admin',
        'PASSWORD': '//BT29042025&&',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
# config/settings.py
AUTH_USER_MODEL = 'usuarios.Usuario'

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_L10N = True
USE_TZ = True
USE_THOUSAND_SEPARATOR = True
DECIMAL_SEPARATOR = '.'
THOUSAND_SEPARATOR = ','
# 16,186.20
# 20,483.20
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

# config/settings.py

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# config/settings.py

# Configuración de correo electrónico (ajustar según proveedor)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # o el servidor SMTP que uses
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'marcovazquezdelgado.movilidad@gmail.com'  # correo desde el que se envían las notificaciones
EMAIL_HOST_PASSWORD = 'tu_contraseña'  # contraseña o clave de aplicación
#DEFAULT_FROM_EMAIL = 'Bolsa de Trabajo <noreply@bolsadetrabajo.example.com>'
DEFAULT_FROM_EMAIL = 'Bolsa de Trabajo marcovazquezdelgado.movilidad@gmail.com>'

# Para desarrollo, puedes usar el backend de consola (muestra emails en la terminal)
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'