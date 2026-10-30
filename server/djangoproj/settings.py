import os
from pathlib import Path
BASE_DIR=Path(__file__).resolve().parent.parent
SECRET_KEY=os.getenv("DJANGO_SECRET_KEY","local-development-only-change-before-deployment")
DEBUG=os.getenv("DJANGO_DEBUG","true").lower()=="true"
ALLOWED_HOSTS=os.getenv("DJANGO_ALLOWED_HOSTS","localhost,127.0.0.1").split(",")
CSRF_TRUSTED_ORIGINS=[x for x in os.getenv("CSRF_TRUSTED_ORIGINS","").split(",") if x]
INSTALLED_APPS=["djangoapp.apps.DjangoappConfig","django.contrib.admin","django.contrib.auth","django.contrib.contenttypes","django.contrib.sessions","django.contrib.messages","django.contrib.staticfiles"]
MIDDLEWARE=["django.middleware.security.SecurityMiddleware","whitenoise.middleware.WhiteNoiseMiddleware","django.contrib.sessions.middleware.SessionMiddleware","django.middleware.common.CommonMiddleware","django.contrib.auth.middleware.AuthenticationMiddleware","django.contrib.messages.middleware.MessageMiddleware","django.middleware.clickjacking.XFrameOptionsMiddleware"]
ROOT_URLCONF="djangoproj.urls"
TEMPLATES=[{"BACKEND":"django.template.backends.django.DjangoTemplates","DIRS":[BASE_DIR/"frontend/build",BASE_DIR/"frontend/static"],"APP_DIRS":True,"OPTIONS":{"context_processors":["django.template.context_processors.debug","django.template.context_processors.request","django.contrib.auth.context_processors.auth","django.contrib.messages.context_processors.messages"]}}]
WSGI_APPLICATION="djangoproj.wsgi.application"
DATABASES={"default":{"ENGINE":"django.db.backends.sqlite3","NAME":os.getenv("SQLITE_PATH",str(BASE_DIR/"db.sqlite3"))}}
AUTH_PASSWORD_VALIDATORS=[{"NAME":"django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},{"NAME":"django.contrib.auth.password_validation.MinimumLengthValidator"},{"NAME":"django.contrib.auth.password_validation.CommonPasswordValidator"},{"NAME":"django.contrib.auth.password_validation.NumericPasswordValidator"}]
LANGUAGE_CODE="en-us"
TIME_ZONE="UTC"
USE_I18N=True
USE_TZ=True
STATIC_URL="/static/"
STATIC_ROOT=BASE_DIR/"static"
STATICFILES_DIRS=[BASE_DIR/"frontend/static"]
if (BASE_DIR/"frontend/build/assets").exists():
    STATICFILES_DIRS.append(("assets",BASE_DIR/"frontend/build/assets"))
DEFAULT_AUTO_FIELD="django.db.models.BigAutoField"
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE="Lax"
SESSION_COOKIE_SECURE=os.getenv("COOKIE_SECURE","false").lower()=="true"
SECURE_PROXY_SSL_HEADER=("HTTP_X_FORWARDED_PROTO","https")
