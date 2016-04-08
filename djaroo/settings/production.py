# for application djaroo_exp1
#  static is here: djaroo_exp1_static
# mysql -- exp1db
# db username -- amir_exp1
# password -- firstexp2280djarooproject
# webfaction ssh: username=amirtz ; password=long012B2848short!@elad

# superuser: username=djaroo_admin ; password=become@3737!dont#ativ050run1987%

"""
    Django settings for exp1 project.

    Generated by 'django-admin startproject' using Django 1.8.5.

    For more information on this file, see
    https://docs.djangoproject.com/en/1.8/topics/settings/

    For the full list of settings and their values, see
    https://docs.djangoproject.com/en/1.8/ref/settings/
"""

from django.conf import settings

if not settings.DEBUG:
    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    import os

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = '3eywp!rth*c)5*(hx=lv=dzfxu6!+t%(*^til2uuwd&cnmo+gr'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = False

    ALLOWED_HOSTS = ['djaroo.com', 'www.djaroo.com']

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
        # 'allauth',
        # 'allauth.account',
        # 'allauth.socialaccount',
        # 'allauth.socialaccount.providers.facebook',
        # 'allauth.socialaccount.providers.google',
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
            'NAME': 'djaroodb',
            'USER': 'amir_exp1',
            'PASSWORD': 'firstexp2280djarooproject',
            # 'HOST': '127.0.0.1',
            # 'PORT': '3306',
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

    STATIC_ROOT = '/home/amirtz/webapps/djaroo_static/'
    # os.path.join(os.path.dirname(BASE_DIR), "static_in_env", "static_root")

    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, "static_in_pro", "our_static"),
        # os.path.join(BASE_DIR, "static_in_env"),
        # '/var/www/static/',
    )

    MEDIA_URL = '/media/'
    MEDIA_ROOT = '/home/amirtz/webapps/djaroo_media/'
    # os.path.join(os.path.dirname(BASE_DIR), "static_in_env", "media_root")

    SITE_ID = 1

    # Allauth settings
    AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend"
    )

    # auth allauth configurations
    # after logging in, redirect the user to the home page
    LOGIN_REDIRECT_URL = '/success_close'

    # auth providers
    SOCIALACCOUNT_PROVIDERS = {
        'facebook': {
            'SCOPE': ['email', 'public_profile'],
            'METHOD': 'js_sdk',  # instead of 'oauth2'
            # need to add the info you want to SCOPE as well
            # available SCOPE: https://developers.facebook.com/docs/facebook-login/permissions
            # 'FIELDS': [
            # ],
        },
        'google': {
            'SCOPE': ['email', 'profile'],
            'AUTH_PARAMS': {'access_type': 'online'}
        }
    }

    # auto send verification email
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

    ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
    ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
    ACCOUNT_USERNAME_REQUIRED = True
    ACCOUNT_EMAIL_REQUIRED = True

    SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
    # ask socialaccount for user's email
    SOCIALACCOUNT_QUERY_EMAIL = True
    # Attempt to bypass the signup form by using fields (e.g. username, email)
    # retrieved from the social account provider.
    # If a conflict arises due to a duplicate e-mail address the signup form will still kick in.
    # if setting it to false - sometimes register users as username = user
    SOCIALACCOUNT_AUTO_SIGNUP = False
    SOCIALACCOUNT_EMAIL_REQUIRED = False
