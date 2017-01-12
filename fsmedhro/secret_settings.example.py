# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ADD YOUR OWN SECRET_KEY HERE'  # <--- change to your settings

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'fsmedhro',
        'USER': 'USERNAME',  # <--- change to your settings
        'PASSWORD': 'PASSWORD',  # <--- change to your settings
        'HOST': 'localhost',
        'PORT': '',
    }
}