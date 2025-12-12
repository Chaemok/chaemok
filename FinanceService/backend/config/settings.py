# Django settings for config project.

from pathlib import Path
import os
from datetime import timedelta
import dj_database_url # 🚨 [추가] PostgreSQL 연결을 위해 필요
from django.core.management.utils import get_random_secret_key # 🚨 [추가] SECRET_KEY 생성용

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# ----------------------------------------------------
# 1. 시크릿 키 (SECRET_KEY) 및 디버그 모드 설정
# ----------------------------------------------------
# 🚨 [수정] Railway 환경 변수 'SECRET_KEY'에서 가져오고, 없으면 랜덤 생성
SECRET_KEY = os.environ.get('SECRET_KEY', get_random_secret_key())

# 🚨 [수정] DEBUG 모드는 환경 변수에서 가져오며, 기본값은 False (배포 기준)
DEBUG = os.environ.get('DEBUG', 'False') == 'True'


# ----------------------------------------------------
# 2. 호스트 및 CORS 설정 (Railway/Vercel 연동)
# ----------------------------------------------------
# 🚨 [수정] Vercel과 Railway 도메인을 환경 변수에서 가져와 허용
VERCEL_DOMAIN = os.environ.get('VERCEL_DOMAIN', 'http://localhost:5173')
RAILWAY_DOMAIN = os.environ.get('RAILWAY_DOMAIN', '127.0.0.1')

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    RAILWAY_DOMAIN,
    '.railway.app', # Railway에서 제공하는 서브 도메인 허용
    VERCEL_DOMAIN.replace('https://', '').replace('http://', '').split('/')[0], # Vercel 도메인 허용
]

# 🚨 [수정] CORS 설정: Vercel 도메인 허용 (http/https 무관하게)
CORS_ALLOWED_ORIGINS = [
    VERCEL_DOMAIN.replace('http://', 'https://'), # https:// 프론트엔드 도메인
    VERCEL_DOMAIN.replace('https://', 'http://'), # http:// 프론트엔드 도메인
    "http://localhost:5173",   # Vue 개발 서버
    "http://127.0.0.1:5173",
]
CORS_ALLOW_CREDENTIALS = True # 인증 정보(쿠키, 인증 헤더 등) 전달 허용


# Application definition

INSTALLED_APPS = [
    # 🚨 [추가] 정적 파일 처리를 위한 Whitenoise
    'whitenoise.runserver_nostatic', 
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders', #배포
    
    # Local apps 
    'accounts',
    'posts',
    'finances',
    'maps',
]


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # CORS
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # 🚨 [추가] 정적 파일 처리를 위한 Whitenoise
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [], # 템플릿 경로를 명시적으로 비워둠 (앱 폴더에서 찾도록)
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug', # debug context 추가
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# ----------------------------------------------------
# 3. 데이터베이스 (PostgreSQL for Railway)
# ----------------------------------------------------
# 🚨 [수정] Railway에서 자동 제공하는 DATABASE_URL 환경 변수를 사용하도록 설정
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', f'sqlite:///{BASE_DIR / "db.sqlite3"}'),
        conn_max_age=600  # 연결 유지 시간
    )
}


# ... (Password validation 설정은 그대로 유지) ...
# ... (Internationalization 설정은 그대로 유지) ...


# ----------------------------------------------------
# 4. 정적 파일 (Static files) 설정
# ----------------------------------------------------
# 🚨 [수정] 배포 시 정적 파일을 수집할 경로 지정 (Whitenoise 사용)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# 🚨 [추가] Whitenoise 설정 (gzip 압축 및 캐시 헤더)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# 이미지/파일 업로드 설정
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ... (REST_FRAMEWORK 설정은 그대로 유지) ...

# ----------------------------------------------------
# 5. Custom User Model 및 Allauth 설정
# ----------------------------------------------------
AUTH_USER_MODEL = 'accounts.User'
LOGIN_REDIRECT_URL = '/'          
ACCOUNT_LOGOUT_REDIRECT_URL = '/' 

# 🚨 [수정] allauth 설정 (원래 설정대로 유지)
# 기존에 'mandatory'나 'optional'로 되어 있다면 'none'으로 변경
ACCOUNT_EMAIL_VERIFICATION = 'none' 
ACCOUNT_AUTHENTICATION_METHOD = 'username' 
ACCOUNT_EMAIL_REQUIRED = False