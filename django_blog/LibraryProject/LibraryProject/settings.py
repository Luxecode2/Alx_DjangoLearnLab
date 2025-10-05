import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-your-secret-key-for-testing' # IMPORTANT: CHANGE THIS IN PRODUCTION

# Step 1: Configure Secure Settings
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False # Must be False for production

# Allowed hosts for the Django application. Crucial when DEBUG is False.
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com', '127.0.0.1', 'localhost']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'csp', # Step 4: Add django-csp to INSTALLED_APPS
    'bookshelf', # Your application
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'csp.middleware.CSPMiddleware', # Step 4: Add CSPMiddleware after SessionMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'LibraryProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'LibraryProject.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root') # Where `collectstatic` will put files

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root') # Where user-uploaded files go


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model from Task 1
AUTH_USER_MODEL = 'bookshelf.CustomUser'

# --- Task 3: Security Best Practices Configuration ---

# Step 1: Configure Secure Settings

# Enables browser's XSS filter.
SECURE_BROWSER_XSS_FILTER = True
# Prevents clickjacking by forbidding embedding the site in an iframe.
X_FRAME_OPTIONS = 'DENY'
# Prevents browsers from MIME-sniffing content-types away from the declared Content-Type.
SECURE_CONTENT_TYPE_NOSNIFF = True

# Ensures CSRF cookies are only sent over HTTPS. (Also part of Task 4)
CSRF_COOKIE_SECURE = True
# Ensures session cookies are only sent over HTTPS. (Also part of Task 4)
SESSION_COOKIE_SECURE = True

# Step 4: Implement Content Security Policy (CSP)
# You need to install 'django-csp' (pip install django-csp) and add 'csp' to INSTALLED_APPS.
# These directives specify valid sources for different types of content.
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'",) # Explicitly allow scripts from self. Add 'unsafe-inline' only if absolutely necessary and temporary.
CSP_STYLE_SRC = ("'self'",) # Explicitly allow styles from self. Add 'unsafe-inline' only if absolutely necessary and temporary.
CSP_IMG_SRC = ("'self'", 'data:',) # Allows images from self and data URIs (e.g., small embedded images).
CSP_FONT_SRC = ("'self'",)
CSP_CONNECT_SRC = ("'self'",)
CSP_OBJECT_SRC = ("'none'",) # Prevents embedding Flash, Java applets, etc.
CSP_BASE_URI = ("'self'",) # Restricts the URLs that can be used in a document's <base> element.
CSP_FRAME_ANCESTORS = ("'self'",) # Specifies valid parents that may embed the page (consistent with X_FRAME_OPTIONS).

# Uncomment these for reporting CSP violations (for development/monitoring)
# CSP_REPORT_ONLY = True # Report violations without blocking them
# CSP_REPORT_URI = '/csp-report/' # You'd need a view to handle these reports