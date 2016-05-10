from django.conf import settings

"""
Djaroo local settings
"""

if settings.DEBUG:

    import os

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = '3eywp!rth*c)5*(hx=lv=dzfxu6!+t%(*^til2uuwd&cnmo+gr'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    ALLOWED_HOSTS = []

    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = 'djaroo.superuser@gmail.com'
    # Google 2 step verification code, so we wont have to turn down our security level
    EMAIL_HOST_PASSWORD = 'gbaqdkwujzrdlzky'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True

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
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        'allauth.socialaccount.providers.facebook',
        'allauth.socialaccount.providers.google',
        'allauth.socialaccount.providers.twitter',
        # my apps
        'consult',
        'apis',
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
                    # allauth
                    'allauth.account.context_processors.account',
                    'allauth.socialaccount.context_processors.socialaccount',
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'djaroo.wsgi.application'

    # Database
    #  https://docs.djangoproject.com/en/1.8/ref/settings/#databases

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
    )

    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_in_env", "media_root")

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
    # A string pointing to a custom form class (e.g. ‘myapp.forms.SignupForm’)
    # that is used during signup to ask the user for additional input (e.g. newsletter signup, birth date).
    # This class should implement a def signup(self, request, user) method,
    # where user represents the newly signed up user.
    # ACCOUNT_SIGNUP_FORM_CLASS = 'consult.forms.SignupForm'
