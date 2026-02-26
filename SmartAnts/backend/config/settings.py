from pathlib import Path
import os
import dj_database_url

# =====================================================
# BASE DIR
# =====================================================
BASE_DIR = Path(__file__).resolve().parent.parent


# =====================================================
# SECURITY / DEBUG (Render 환경 대응)
# =====================================================
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
DEBUG = os.environ.get("DEBUG", "True").lower() == "true"

ALLOWED_HOSTS = ["127.0.0.1", "localhost", ".onrender.com"]
RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# =====================================================
# GMS (Gemini) - 환경 변수 우선
# =====================================================
GMS_KEY = os.environ.get("GMS_KEY", "S14P02DB09-afa432ce-5c10-4b60-8f6b-3273cace779a")
GMS_ENDPOINT_BASE = (
    "https://gms.ssafy.io/gmsapi/"
    "generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.0-flash:generateContent"
)

YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", "AIzaSyAJbfefA6rNy64Bm-qgJHe2vvvFh1sBZvE")


# =====================================================
# APPLICATION
# =====================================================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",

    # Third-party
    "rest_framework",
    "rest_framework.authtoken",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "corsheaders",

    "allauth",
    "allauth.account",
    "allauth.socialaccount",

    # Local apps
    "accounts",
    "community",
    "finlife",
    "map",
    "chatbot",
]

SITE_ID = 1


# =====================================================
# MIDDLEWARE
# =====================================================
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]


# =====================================================
# CORS / CSRF (Render/Vercel 대응)
# =====================================================
CORS_ALLOW_ALL_ORIGINS = True  # 배포 단계에서는 필요한 도메인만 허용하는 것을 권장합니다.
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

FRONTEND_URL = os.environ.get("FRONTEND_URL")
if FRONTEND_URL:
    CSRF_TRUSTED_ORIGINS.append(FRONTEND_URL)


# =====================================================
# URL / TEMPLATE
# =====================================================
ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "config.wsgi.application"


# =====================================================
# DATABASE (SQLite + Render Postgres 지원)
# =====================================================
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}


# =====================================================
# AUTH / ALLAUTH
# =====================================================
AUTH_USER_MODEL = "accounts.User"

LOGIN_REDIRECT_URL = "/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/"

ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_AUTHENTICATION_METHOD = "username"
ACCOUNT_EMAIL_REQUIRED = False

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

APPEND_SLASH = True

REST_AUTH = {
    "REGISTER_SERIALIZER": "accounts.serializers.CustomRegisterSerializer",
    "USER_DETAILS_SERIALIZER": "accounts.serializers.CustomUserDetailsSerializer",
}


# =====================================================
# REST FRAMEWORK
# =====================================================
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}


# =====================================================
# STATIC / MEDIA
# =====================================================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# WhiteNoise storage for compressed/cached files
if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# =====================================================
# ETC
# =====================================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LANGUAGE_CODE = "ko-kr"
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_TZ = True
