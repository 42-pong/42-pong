"""
Django settings for pong project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# todo mypyが型対応していない3rdパーティのライブラリも型対応できるようにする
import environ  # type: ignore

# 環境変数のスキーマを定義
env = environ.Env(
    DEBUG=(bool, False),
    # 自動テストで例外処理になるためSECRET_KEYを定義
    SECRET_KEY=(str, "your-default-secret-key"),
    DB_NAME=(str, "db_name"),
    DB_USER=(str, "db_user"),
    DB_PASSWORD=(str, "db_password"),
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# .envファイルを探し、読み込む
env_file = Path(BASE_DIR) / ".env"
environ.Env.read_env(env_file)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

DEBUG = env("DEBUG")

SECRET_KEY = env("SECRET_KEY")


ALLOWED_HOSTS: list[str] = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party apps
    "rest_framework",
    "drf_spectacular",  # for Swagger UI
    "drf_spectacular_sidecar",  # for Swagger UI
    # apps
    "jwt_token",
    "accounts",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "pong.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "pong.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": "db",  # compose.yamlのDBのservice名
        "PORT": "5432",  # postgresのデフォルトポート
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Tokyo"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Django REST framework
# https://drf-spectacular.readthedocs.io/en/latest/readme.html

REST_FRAMEWORK = {
    # view setやserializerから自動的にOpenAPI3.0スキーマを生成
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    # djangorestframework_simplejwt
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}

SPECTACULAR_SETTINGS = {
    # drf_spectacular
    "TITLE": "Pong API",
    "DESCRIPTION": "The Pong API provides backend services for the Pong game.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": True,  # スキーマのendpointを有効にする
    # drf_spectacular_sidecar
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    # djangorestframework_simplejwt
    "AUTHENTICATION_WHITELIST": [
        "rest_framework_simplejwt.authentication.JWTAuthentication"
    ],
}
