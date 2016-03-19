__author__ = 'Amir'
"""
Django settings for exp1 project.

Generated by 'django-admin startproject' using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3eywp!rth*c)5*(hx=lv=dzfxu6!+t%(*^til2uuwd&cnmo+gr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'tzuramir@gmail.com'
EMAIL_HOST_PASSWORD = '0547918841A'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# if using gmail account -> unlock Captcha (security level)

# Application definition

INSTALLED_APPS = (
    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third party apps
    # allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.twitter',
    # 'crispy_forms',
    # 'registration',
    # my apps
    'consult',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'djaroo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'allauth.account.context_processors.account',
                'allauth.socialaccount.context_processors.socialaccount',
            ],
        },
    },
]

WSGI_APPLICATION = 'djaroo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        # 'NAME': os.path.join(BASE_DIR, 'db.exp1db'),
        'NAME': 'djarooDB',
        'USER': 'root',
        'PASSWORD': '1234',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_in_env", "static_root")

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static_in_pro", "our_static"),
    # os.path.join(BASE_DIR, "static_in_env"),
    # '/var/www/static/',
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_in_env", "media_root")

# crispy forms TAGs SETTINGS
# CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Django registration-redux settings
# ACCOUNT_ACTIVATION_DAYS = 7
# REGISTRATION_AUTO_LOGIN = True

# Allauth settings
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend"
)

SITE_ID = 1

# auth and allauth settings
# after logging in, redirect the user to the home page
LOGIN_REDIRECT_URL = '/'
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['email', 'public_profile'],
        'METHOD': 'js_sdk',  # instead of 'oauth2'
        # 'FIELDS': ['id',
        #            'email',
        #            'name',
        #            'first_name',
        #            'last_name',
        #            'verified',
        #            'locale',
        #            'timezone',
        #            'link',
        #            'gender',
        #            'updated_time'],
    },
    'google': {
        'SCOPE': ['email', 'profile'],
        'AUTH_PARAMS': {'access_type': 'online'}
    }
}

# auto send verification email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_REQUIRED = False
SOCIALACCOUNT_AUTO_SIGNUP = False

# A string pointing to a custom form class (e.g. �myapp.forms.SignupForm�)
# that is used during signup to ask the user for additional input (e.g. newsletter signup, birth date).
# This class should implement a def signup(self, request, user) method,
# where user represents the newly signed up user.
# ACCOUNT_SIGNUP_FORM_CLASS = 'consult.forms.SignupForm'
