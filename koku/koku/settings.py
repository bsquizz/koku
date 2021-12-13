#
# Copyright 2021 Red Hat Inc.
# SPDX-License-Identifier: Apache-2.0
#
"""
Django settings for koku project.

Generated by 'django-admin startproject' using Django 2.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
import logging
import os
import sys
from json import JSONDecodeError

from boto3.session import Session
from botocore.exceptions import ClientError
from corsheaders.defaults import default_headers

from . import database
from . import sentry
from .configurator import CONFIGURATOR
from .env import ENVIRONMENT


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# The SECRET_KEY is provided via an environment variable in OpenShift
SECRET_KEY = ENVIRONMENT.get_value(
    "DJANGO_SECRET_KEY",
    # safe value used for development when DJANGO_SECRET_KEY might not be set
    default="asvuhxowz)zjbo4%7pc$ek1nbfh_-#%$bq_x8tkh=#e24825=5",
)

# SECURITY WARNING: don't run with debug turned on in production!
# Default value: False
DEBUG = ENVIRONMENT.bool("DEVELOPMENT", default=False)

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    # django
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third-party
    "rest_framework",
    "django_extensions",
    "django_filters",
    "corsheaders",
    "querystring_parser",
    "django_prometheus",
    # local apps
    "api",
    "hcs",
    "masu",
    "reporting",
    "reporting_common",
    "cost_models",
    "sources",
    "tenant_schemas",
]

SILENCED_SYSTEM_CHECKS = ["tenant_schemas.W001"]

SHARED_APPS = (
    "tenant_schemas",
    "api",
    "masu",
    "reporting_common",
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "rest_framework",
    "sources",
)

TENANT_APPS = ("reporting", "cost_models")

DEFAULT_FILE_STORAGE = "tenant_schemas.storage.TenantFileSystemStorage"

ACCOUNT_ENHANCED_METRICS = ENVIRONMENT.bool("ACCOUNT_ENHANCED_METRICS", default=False)

PROMETHEUS_BEFORE_MIDDLEWARE = "django_prometheus.middleware.PrometheusBeforeMiddleware"
PROMETHEUS_AFTER_MIDDLEWARE = "django_prometheus.middleware.PrometheusAfterMiddleware"

if ACCOUNT_ENHANCED_METRICS:
    PROMETHEUS_BEFORE_MIDDLEWARE = "koku.middleware.AccountEnhancedMetricsBeforeMiddleware"
    PROMETHEUS_AFTER_MIDDLEWARE = "koku.middleware.AccountEnhancedMetricsAfterMiddleware"

### Middleware setup
MIDDLEWARE = [
    PROMETHEUS_BEFORE_MIDDLEWARE,
    "koku.middleware.RequestTimingMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "koku.middleware.DisableCSRF",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "koku.middleware.IdentityHeaderMiddleware",
    "koku.middleware.KokuTenantMiddleware",
    "koku.middleware.KokuTenantSchemaExistsMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    PROMETHEUS_AFTER_MIDDLEWARE,
]

DEVELOPMENT = ENVIRONMENT.bool("DEVELOPMENT", default=False)
if DEVELOPMENT:
    DEFAULT_IDENTITY = {
        "identity": {
            "account_number": "10001",
            "type": "User",
            "user": {"username": "user_dev", "email": "user_dev@foo.com", "is_org_admin": "True", "access": {}},
        },
        "entitlements": {"cost_management": {"is_entitled": "True"}},
    }
    DEVELOPMENT_IDENTITY = ENVIRONMENT.json("DEVELOPMENT_IDENTITY", default=DEFAULT_IDENTITY)
    MIDDLEWARE.insert(5, "koku.dev_middleware.DevelopmentIdentityHeaderMiddleware")
    MIDDLEWARE.insert(len(MIDDLEWARE) - 1, "django_cprofile_middleware.middleware.ProfilerMiddleware")
    DJANGO_CPROFILE_MIDDLEWARE_REQUIRE_STAFF = False

### Feature Flags
UNLEASH_HOST = CONFIGURATOR.get_feature_flag_host()
UNLEASH_PORT = CONFIGURATOR.get_feature_flag_port()
UNLEASH_PREFIX = "https" if str(UNLEASH_PORT) == "443" else "http"
UNLEASH_URL = f"{UNLEASH_PREFIX}://{UNLEASH_HOST}:{UNLEASH_PORT}/api"
UNLEASH_TOKEN = CONFIGURATOR.get_feature_flag_token()
UNLEASH_CACHE_DIR = ENVIRONMENT.get_value("UNLEASH_CACHE_DIR", default=os.path.join(BASE_DIR, "..", ".unleash"))

### Currency URL
CURRENCY_URL = ENVIRONMENT.get_value("CURRENCY_URL", default="https://open.er-api.com/v6/latest/USD")

### End Middleware

AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.AllowAllUsersModelBackend"]

MASU = ENVIRONMENT.bool("MASU", default=False)
SOURCES = ENVIRONMENT.bool("SOURCES", default=False)
ROOT_URLCONF = "koku.urls"
if MASU:
    ROOT_URLCONF = "masu.urls"
elif SOURCES:
    ROOT_URLCONF = "sources.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "koku.wsgi.application"

WORKER_CACHE_KEY = "worker"
WORKER_CACHE_TIMEOUT = ENVIRONMENT.get_value("WORKER_CACHE_TIMEOUT", default=3600)
CACHE_MIDDLEWARE_SECONDS = ENVIRONMENT.get_value("CACHE_TIMEOUT", default=3600)

HOSTNAME = ENVIRONMENT.get_value("HOSTNAME", default="localhost")

REDIS_HOST = CONFIGURATOR.get_in_memory_db_host()
REDIS_PORT = CONFIGURATOR.get_in_memory_db_port()
REDIS_DB = 1
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

KEEPDB = ENVIRONMENT.bool("KEEPDB", default=True)
TEST_CACHE_LOCATION = "unique-snowflake"
if "test" in sys.argv:
    TEST_RUNNER = "koku.koku_test_runner.KokuTestRunner"
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": TEST_CACHE_LOCATION,
            "KEY_FUNCTION": "tenant_schemas.cache.make_key",
            "REVERSE_KEY_FUNCTION": "tenant_schemas.cache.reverse_key",
        },
        "rbac": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache", "LOCATION": TEST_CACHE_LOCATION},
        "worker": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache", "LOCATION": TEST_CACHE_LOCATION},
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
            "KEY_FUNCTION": "tenant_schemas.cache.make_key",
            "REVERSE_KEY_FUNCTION": "tenant_schemas.cache.reverse_key",
            "TIMEOUT": 3600,  # 1 hour default
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "IGNORE_EXCEPTIONS": True,
                "MAX_ENTRIES": 1000,
            },
        },
        "rbac": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/1",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "IGNORE_EXCEPTIONS": True,
                "MAX_ENTRIES": 1000,
            },
        },
        "worker": {
            "BACKEND": "django.core.cache.backends.db.DatabaseCache",
            "LOCATION": "worker_cache_table",
            "TIMEOUT": 86400,  # 24 hours
        },
    }

if ENVIRONMENT.bool("CACHED_VIEWS_DISABLED", default=False):
    CACHES.update({"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}})
DATABASES = {"default": database.config()}

DATABASE_ROUTERS = ("tenant_schemas.routers.TenantSyncRouter",)

# Hive DB variables
HIVE_DATABASE_USER = ENVIRONMENT.get_value("HIVE_DATABASE_USER", default="hive")
HIVE_DATABASE_NAME = ENVIRONMENT.get_value("HIVE_DATABASE_NAME", default="hive")
HIVE_DATABASE_PASSWORD = ENVIRONMENT.get_value("HIVE_DATABASE_PASSWORD", default="hive")

#
TENANT_MODEL = "api.Tenant"

PROMETHEUS_EXPORT_MIGRATIONS = False

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

API_PATH_PREFIX = ENVIRONMENT.get_value("API_PATH_PREFIX", default="/api")
DEFAULT_RETAIN_NUM_MONTHS = 4
RETAIN_NUM_MONTHS = ENVIRONMENT.int("RETAIN_NUM_MONTHS", default=DEFAULT_RETAIN_NUM_MONTHS)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "{}/static/".format(API_PATH_PREFIX.rstrip("/"))

STATICFILES_DIRS = [os.path.join(BASE_DIR, "..", "docs/source/specs")]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

INTERNAL_IPS = ["127.0.0.1"]

DEFAULT_PAGINATION_CLASS = "api.common.pagination.StandardResultsSetPagination"
DEFAULT_EXCEPTION_HANDLER = "api.common.exception_handler.custom_exception_handler"

DEFAULT_RENDERER_CLASSES = ("rest_framework.renderers.JSONRenderer", "api.common.csv.PaginatedCSVRenderer")

if DEVELOPMENT:
    DEFAULT_RENDERER_CLASSES = DEFAULT_RENDERER_CLASSES + ("rest_framework.renderers.BrowsableAPIRenderer",)

# django rest_framework settings
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"],
    "DEFAULT_PAGINATION_CLASS": DEFAULT_PAGINATION_CLASS,
    "DEFAULT_RENDERER_CLASSES": DEFAULT_RENDERER_CLASSES,
    "EXCEPTION_HANDLER": DEFAULT_EXCEPTION_HANDLER,
}

CW_AWS_ACCESS_KEY_ID = CONFIGURATOR.get_cloudwatch_access_id()
CW_AWS_SECRET_ACCESS_KEY = CONFIGURATOR.get_cloudwatch_access_key()
CW_AWS_REGION = CONFIGURATOR.get_cloudwatch_region()
CW_LOG_GROUP = CONFIGURATOR.get_cloudwatch_log_group()

LOGGING_FORMATTER = ENVIRONMENT.get_value("DJANGO_LOG_FORMATTER", default="simple")
DJANGO_LOGGING_LEVEL = ENVIRONMENT.get_value("DJANGO_LOG_LEVEL", default="INFO")
KOKU_LOGGING_LEVEL = ENVIRONMENT.get_value("KOKU_LOG_LEVEL", default="INFO")
UNLEASH_LOGGING_LEVEL = ENVIRONMENT.get_value("UNLEASH_LOG_LEVEL", default="WARNING")
LOGGING_HANDLERS = ENVIRONMENT.get_value("DJANGO_LOG_HANDLERS", default="console").split(",")
VERBOSE_FORMATTING = (
    "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d "
    "%(task_id)s %(task_parent_id)s %(task_root_id)s "
    "%(message)s"
)
SIMPLE_FORMATTING = "[%(asctime)s] %(levelname)s %(task_root_id)s %(message)s"

LOG_DIRECTORY = ENVIRONMENT.get_value("LOG_DIRECTORY", default=BASE_DIR)
DEFAULT_LOG_FILE = os.path.join(LOG_DIRECTORY, "app.log")
LOGGING_FILE = ENVIRONMENT.get_value("DJANGO_LOG_FILE", default=DEFAULT_LOG_FILE)

if CW_AWS_ACCESS_KEY_ID:
    try:
        POD_NAME = ENVIRONMENT.get_value("APP_POD_NAME", default="local")
        BOTO3_SESSION = Session(
            aws_access_key_id=CW_AWS_ACCESS_KEY_ID,
            aws_secret_access_key=CW_AWS_SECRET_ACCESS_KEY,
            region_name=CW_AWS_REGION,
        )
        watchtower = BOTO3_SESSION.client("logs")
        watchtower.create_log_stream(logGroupName=CW_LOG_GROUP, logStreamName=POD_NAME)
        LOGGING_HANDLERS += ["watchtower"]
        WATCHTOWER_HANDLER = {
            "level": KOKU_LOGGING_LEVEL,
            "class": "watchtower.CloudWatchLogHandler",
            "boto3_session": BOTO3_SESSION,
            "log_group": CW_LOG_GROUP,
            "stream_name": POD_NAME,
            "formatter": LOGGING_FORMATTER,
            "use_queues": False,
            "create_log_group": False,
        }
    except ClientError as e:
        if e.response.get("Error", {}).get("Code") == "ResourceAlreadyExistsException":
            LOGGING_HANDLERS += ["watchtower"]
            WATCHTOWER_HANDLER = {
                "level": KOKU_LOGGING_LEVEL,
                "class": "watchtower.CloudWatchLogHandler",
                "boto3_session": BOTO3_SESSION,
                "log_group": CW_LOG_GROUP,
                "stream_name": POD_NAME,
                "formatter": LOGGING_FORMATTER,
                "use_queues": False,
                "create_log_group": False,
            }
        else:
            print("CloudWatch not configured.")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"()": "koku.log.TaskFormatter", "format": VERBOSE_FORMATTING},
        "simple": {"()": "koku.log.TaskFormatter", "format": SIMPLE_FORMATTING},
    },
    "handlers": {
        "celery": {"class": "logging.StreamHandler", "formatter": LOGGING_FORMATTER},
        "console": {"class": "logging.StreamHandler", "formatter": LOGGING_FORMATTER},
        "file": {
            "level": KOKU_LOGGING_LEVEL,
            "class": "logging.FileHandler",
            "filename": LOGGING_FILE,
            "formatter": LOGGING_FORMATTER,
        },
    },
    "loggers": {
        "django": {"handlers": LOGGING_HANDLERS, "level": DJANGO_LOGGING_LEVEL},
        "api": {"handlers": LOGGING_HANDLERS, "level": KOKU_LOGGING_LEVEL},
        "celery": {"handlers": LOGGING_HANDLERS, "level": KOKU_LOGGING_LEVEL, "propagate": False},
        "cost_models": {"handlers": LOGGING_HANDLERS, "level": KOKU_LOGGING_LEVEL},
        "forecast": {"handlers": LOGGING_HANDLERS, "level": KOKU_LOGGING_LEVEL},
        "kafka_utils": {"handlers": LOGGING_HANDLERS, "level": KOKU_LOGGING_LEVEL},
        "koku": {"handlers": LOGGING_HANDLERS, "level": KOKU_LOGGING_LEVEL},
        "providers": {"handlers": LOGGING_HANDLERS, "level": KOKU_LOGGING_LEVEL},
        "reporting": {"handlers": LOGGING_HANDLERS, "level": KOKU_LOGGING_LEVEL},
        "reporting_common": {"handlers": LOGGING_HANDLERS, "level": KOKU_LOGGING_LEVEL},
        "masu": {"handlers": LOGGING_HANDLERS, "level": KOKU_LOGGING_LEVEL, "propagate": False},
        "sources": {"handlers": LOGGING_HANDLERS, "level": KOKU_LOGGING_LEVEL},
        # The following set the log level for the UnleashClient and Unleash cache refresh jobs.
        # Setting to WARNING will prevent the INFO level spam.
        "UnleashClient": {"handlers": LOGGING_HANDLERS, "level": UNLEASH_LOGGING_LEVEL},
        "apscheduler": {"handlers": LOGGING_HANDLERS, "level": UNLEASH_LOGGING_LEVEL},
    },
}

if "watchtower" in LOGGING_HANDLERS:
    LOGGING["handlers"]["watchtower"] = WATCHTOWER_HANDLER
    print("CloudWatch configured.")

KOKU_DEFAULT_CURRENCY = ENVIRONMENT.get_value("KOKU_DEFAULT_CURRENCY", default="USD")
KOKU_DEFAULT_COST_TYPE = ENVIRONMENT.get_value("KOKU_DEFAULT_COST_TYPE", default="unblended_cost")
KOKU_DEFAULT_TIMEZONE = ENVIRONMENT.get_value("KOKU_DEFAULT_TIMEZONE", default="UTC")
KOKU_DEFAULT_LOCALE = ENVIRONMENT.get_value("KOKU_DEFAULT_LOCALE", default="en_US.UTF-8")


# Cors Setup
# See https://github.com/ottoyiu/django-cors-headers
CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_HEADERS = default_headers + ("x-rh-identity", "HTTP_X_RH_IDENTITY")

APPEND_SLASH = False

DISABLE_LOGGING = ENVIRONMENT.bool("DISABLE_LOGGING", default=False)
# disable log messages less than CRITICAL when running unit tests.
if len(sys.argv) > 1 and sys.argv[1] == "test" and DISABLE_LOGGING:
    logging.disable(logging.CRITICAL)

# AMQP Message Broker
RABBITMQ_HOST = ENVIRONMENT.get_value("RABBITMQ_HOST", default="localhost")
RABBITMQ_PORT = ENVIRONMENT.get_value("RABBITMQ_PORT", default="5672")


# AWS S3 Bucket Settings
REQUESTED_BUCKET = ENVIRONMENT.get_value("REQUESTED_BUCKET", default="koku-report")
S3_TIMEOUT = ENVIRONMENT.int("S3_CONNECTION_TIMEOUT", default=60)
S3_ENDPOINT = CONFIGURATOR.get_object_store_endpoint()
S3_REGION = ENVIRONMENT.get_value("S3_REGION", default="us-east-1")
S3_BUCKET_PATH = ENVIRONMENT.get_value("S3_BUCKET_PATH", default="data_archive")
S3_BUCKET_NAME = CONFIGURATOR.get_object_store_bucket(REQUESTED_BUCKET)
S3_ACCESS_KEY = CONFIGURATOR.get_object_store_access_key(REQUESTED_BUCKET)
S3_SECRET = CONFIGURATOR.get_object_store_secret_key(REQUESTED_BUCKET)
S3_MINIO_IN_USE = "minio" in S3_ENDPOINT.lower()

ENABLE_S3_ARCHIVING = ENVIRONMENT.bool("ENABLE_S3_ARCHIVING", default=False)
ENABLE_PARQUET_PROCESSING = ENVIRONMENT.bool("ENABLE_PARQUET_PROCESSING", default=False)
PARQUET_PROCESSING_BATCH_SIZE = ENVIRONMENT.int("PARQUET_PROCESSING_BATCH_SIZE", default=200000)
ENABLE_TRINO_SOURCES = ENVIRONMENT.list("ENABLE_TRINO_SOURCES", default=[])
ENABLE_TRINO_ACCOUNTS = ENVIRONMENT.list("ENABLE_TRINO_ACCOUNTS", default=[])
ENABLE_TRINO_SOURCE_TYPE = ENVIRONMENT.list("ENABLE_TRINO_SOURCE_TYPE", default=[])

# Presto Settings
PRESTO_HOST = ENVIRONMENT.get_value("PRESTO_HOST", default=None)
PRESTO_PORT = ENVIRONMENT.get_value("PRESTO_PORT", default=None)
TRINO_DATE_STEP = ENVIRONMENT.int("TRINO_DATE_STEP", default=5)

# IBM Settings
IBM_SERVICE_URL = ENVIRONMENT.get_value("IBM_SERVICE_URL", default="https://enterprise.cloud.ibm.com")

# Time to wait between cold storage retrieval for data export. Default is 3 hours
COLD_STORAGE_RETRIVAL_WAIT_TIME = ENVIRONMENT.int("COLD_STORAGE_RETRIVAL_WAIT_TIME", default=10800)

# Sources Client API Endpoints
KOKU_SOURCES_CLIENT_HOST = CONFIGURATOR.get_endpoint_host("koku", "sources-client", "localhost")
KOKU_SOURCES_CLIENT_PORT = CONFIGURATOR.get_endpoint_port("koku", "sources-client", "4000")
SOURCES_CLIENT_BASE_URL = f"http://{KOKU_SOURCES_CLIENT_HOST}:{KOKU_SOURCES_CLIENT_PORT}/"

# Prometheus pushgateway hostname:port
PROMETHEUS_PUSHGATEWAY = ENVIRONMENT.get_value("PROMETHEUS_PUSHGATEWAY", default="localhost:9091")

# Flag for automatic data ingest on Provider create
AUTO_DATA_INGEST = ENVIRONMENT.bool("AUTO_DATA_INGEST", default=True)

# Demo Accounts list
DEMO_ACCOUNTS = {}
try:
    DEMO_ACCOUNTS = ENVIRONMENT.json("DEMO_ACCOUNTS", default={})
except JSONDecodeError:
    pass

# Aids the UI in showing pre-release features in allowed environments.
# see: koku.api.user_access.view
ENABLE_PRERELEASE_FEATURES = ENVIRONMENT.bool("ENABLE_PRERELEASE_FEATURES", default=False)

# Celery configuration

# Set Broker
CELERY_BROKER_URL = REDIS_URL
USE_RABBIT = ENVIRONMENT.bool("USE_RABBIT", default=False)
if USE_RABBIT:
    CELERY_BROKER_URL = f"amqp://{RABBITMQ_HOST}:{RABBITMQ_PORT}"
    print(f"celery broker using rabbit url: {CELERY_BROKER_URL}")
else:
    print(f"celery broker using redis url: {CELERY_BROKER_URL}")

CELERY_BROKER_CONNECTION_MAX_RETRIES = 400
CELERY_BROKER_CONNECTION_RETRY = True
CELERY_BROKER_POOL_LIMIT = None
CELERY_RESULT_EXPIRES = 28800  # 8 hours (3600 seconds / hour * 8 hours)
CELERY_RESULTS_URL = REDIS_URL
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_WORKER_CONCURRENCY = 1
