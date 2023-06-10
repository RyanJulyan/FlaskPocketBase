import sys, os
from typing import Any, Dict, Union

from dotenv import dotenv_values

from configuration.database_config import (
    DEFAULT_DATABASE_URI,
    PROD_DATABASE_URI,
    DEV_DATABASE_URI,
    TEST_DATABASE_URI,
)

#############################
# Simplify ENVIRON function #
#############################
env = os.environ.get

if getattr(sys, "frozen", False):
    # running as bundle (aka frozen)
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # running live
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    def __init__(self, **kwargs: Any) -> None:
        config = {
            **dotenv_values(
                ".env.shared",
            ),  # load shared environment variables
            **kwargs,  # load passed in variables
            **os.environ,  # override loaded values with environment variables
        }
        self.__dict__.update(config)

    BASE_DIR = BASE_DIR

    ###########################
    # Development environment #
    ###########################
    DEBUG = env("DEBUG", False)
    DEBUG_TB_PROFILER_ENABLED = env("DEBUG_TB_PROFILER_ENABLED", False)
    DEBUG_TB_INTERCEPT_REDIRECTS = env("DEBUG_TB_INTERCEPT_REDIRECTS", False)
    TESTING = env("TESTING", False)

    ##########################
    # Basic Site Information #
    ##########################
    SITE_TITLE = env("SITE_TITLE", "FlaskPocketBase")
    SITE_URL = env("SITE_URL", "http://www.FlaskPocketBase.com")
    SITE_DESCRIPTION = env(
        "SITE_DESCRIPTION", "My awesome new FlaskPocketBase site."
    )
    SITE_THEME_COLOR = env("SITE_THEME_COLOR", "#3367D6")
    DEVELOPER_NAME = env("DEVELOPER_NAME", "FlaskPocketBase")

    ####################################
    # Search Engine Optimization (SEO) #
    ####################################
    SEO_SUBJECT = env("SEO_SUBJECT", "Rapid Application Development.")
    SEO_SUBTITLE = env("SEO_SUBTITLE", "Flask BDA Site.")
    SEO_SUMMARY = env("SEO_SUMMARY", "This site was created using Flask BDA.")
    SEO_ABSTRACT = env(
        "SEO_ABSTRACT", "This site was created using FlaskPocketBase."
    )
    SEO_KEYWORDS = env(
        "SEO_KEYWORDS",
        "Flask, PWA, Python, Rapid Application Development, RAD, Progressive Web App, Flask BDA.",
    )
    SEO_REVISIT_AFTER = env("SEO_REVISIT_AFTER", "7 days")

    ###################
    # List Formatting #
    ###################
    LIST_SEPARATOR = env("LIST_SEPARATOR", ",")

    ########################
    # Date Time Formatting #
    ########################
    #####################################################################################################################################
    # Reference: https://www.journaldev.com/23365/python-string-to-datetime-strptime
    # 'Directive'   Description.	                        Example Output
    # '%a'	        Weekday as locale’s abbreviated name.	Sun, Mon, …, Sat (en_US)So, Mo, …, Sa (de_DE)
    # '%A'	        Weekday as locale’s full name.	Sunday, Monday, …, Saturday (en_US) Sonntag, Montag, …, Samstag (de_DE)
    # '%w'	        Weekday as a decimal number, where 0 is Sunday and 6 is Saturday.	0, 1, 2, 3, 4, 5, 6
    # '%d'	        Day of the month as a zero-padded decimal number.	01, 02, …, 31
    # '%b'	        Month as locale’s abbreviated name.	Jan, Feb, …, Dec (en_US) Jan, Feb, …, Dez (de_DE)
    # '%B'	        Month as locale’s full name.	January, February, …, December (en_US) Januar, Februar, …, Dezember (de_DE)
    # '%m'	        Month as a zero-padded decimal number.	01, 02 … 12
    # '%y'	        Year without century as a zero-padded decimal number.	01, 02, … 99
    # '%Y'	        Year with century as a decimal number.	0001, 0002, … , 9999
    # '%H'	        Hour (24-hour clock) as a zero-padded decimal number.	01, 02, … , 23
    # '%I'	        Hour (12-hour clock) as a zero-padded decimal number.	01, 02, … , 12
    # '%p'	        Locale’s equivalent of either AM or PM.	AM, PM (en_US) am, pm (de_DE)
    # '%M'	        Minute as a zero-padded decimal number.	01, 02, … , 59
    # '%S'	        Second as a zero-padded decimal number.	01, 02, … , 59
    # '%f'	        Microsecond as a decimal number, zero-padded on the left.	000000, 000001, …, 999999 Not applicable with time module.
    # '%z'	        UTC offset in the form ±HHMM[SS] (empty string if the object is naive).	(empty), +0000, -0400, +1030
    # '%Z'	        Time zone name (empty string if the object is naive).	(empty), UTC, IST, CST
    # '%j'	        Day of the year as a zero-padded decimal number.	001, 002, …, 366
    # '%U'	        Week number of the year (Sunday as the first day of the week) as a zero padded decimal number. All days in a new year preceding the first Sunday are considered to be in week 0.	00, 01, …, 53
    # '%W'	        Week number of the year (Monday as the first day of the week) as a decimal number. All days in a new year preceding the first Monday are considered to be in week 0.	00, 01, …, 53
    # '%c'	        Locale’s appropriate date and time representation.	Tue Aug 16 21:30:00 1988 (en_US) Di 16 Aug 21:30:00 1988 (de_DE)
    # '%x'	        Locale’s appropriate date representation.	08/16/88 (None) 08/16/1988 (en_US) 16.08.1988 (de_DE)
    # '%X'	        Locale’s appropriate time representation.	21:30:00 (en_US) 21:30:00 (de_DE)
    # '%%'	        A literal ‘%’ character.	%
    #####################################################################################################################################
    DATE_FORMAT = env("DATE_FORMAT", "%Y/%m/%d")
    TIME_FORMAT = env("TIME_FORMAT", "%H:%M:%S")

    ###################################################
    # Manage SQLALCHEMY_ENGINE_OPTIONS like pool size #
    ###################################################
    # https://docs.sqlalchemy.org/en/13/core/engines.html#sqlalchemy.create_engine.params.pool_pre_ping
    # https://docs.sqlalchemy.org/en/13/core/engines.html#sqlalchemy.create_engine.params.pool_size
    # https://docs.sqlalchemy.org/en/13/core/engines.html#sqlalchemy.create_engine.params.pool_recycle
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": env("POOL_PRE_PING", True),
        "pool_recycle": env("POOL_RECYCLE", -1),
    }

    ##############################################
    # Run create_database() in @app.before_request #
    ##############################################
    AUTO_CREATE_DATABASE = env("AUTO_CREATE_DATABASE", True)

    ##############################################
    # Run db.create_all() in @app.before_request #
    ##############################################
    AUTO_CREATE_TABLES_FROM_MODELS = env(
        "AUTO_CREATE_TABLES_FROM_MODELS", True
    )

    DATABASE_URI = env("DATABASE_URI", DEFAULT_DATABASE_URI)

    SQLALCHEMY_BINDS = {"default": DATABASE_URI}

    SQLALCHEMY_TRACK_MODIFICATIONS = env(
        "SQLALCHEMY_TRACK_MODIFICATIONS", False
    )

    ########################
    # Application threads. #
    ########################
    THREADS_PER_PAGE = env("THREADS_PER_PAGE", 3)

    ############################
    # Time for session expirey #
    ############################
    TIME_TO_EXPIRE = env("TIME_TO_EXPIRE", 3600)

    ################################################################
    # Enable protection agains *Cross-site Request Forgery (CSRF)* #
    ################################################################
    CSRF_ENABLED = env("CSRF_ENABLED", True)
    CSRF_SESSION_KEY = env("CSRF_SESSION_KEY", "secret")

    #############################################
    # Secret key for signing cookies and Tokens #
    #############################################
    SECRET_KEY = env("SECRET_KEY", "secret")
    SECURITY_PASSWORD_SALT = env("SECURITY_PASSWORD_SALT", "secret")

    ################################################
    # Secret key for signing JWT (JSON Web Tokens) #
    ################################################
    JWT_SECRET_KEY = env("JWT_SECRET_KEY", "secret")
    JWT_ACCESS_TOKEN_EXPIRES = env("JWT_ACCESS_TOKEN_EXPIRES", 3600)
    JWT_BLACKLIST_ENABLED = env("JWT_BLACKLIST_ENABLED", True)
    JWT_BLACKLIST_TOKEN_CHECKS = env(
        "JWT_BLACKLIST_TOKEN_CHECKS", ["access", "refresh"]
    )

    ########################
    # CORS ORIGINS allowed #
    ########################
    CORS_ORIGINS = env("CORS_ORIGINS", "*")

    ###############################
    # Default rate limit for site #
    ###############################
    DEFAULT_LIMITS = [
        # "200 per day",
        # "100/day",
        # "500/7days",
        # "50 per hour",
        "3/second",
    ]

    DEFAULT_LIMITS = env("DEFAULT_LIMITS", DEFAULT_LIMITS)

    #####################
    # Email Credentails #
    #####################
    MAIL_SERVER = env("MAIL_SERVER", "smtp.mailtrap.io")
    MAIL_PORT = env("MAIL_PORT", 2525)
    MAIL_USERNAME = env("MAIL_USERNAME", "email@example.com")
    MAIL_PASSWORD = env("MAIL_PASSWORD", "example password")
    MAIL_USE_TLS = env("MAIL_USE_TLS", True)
    MAIL_USE_SSL = env("MAIL_USE_SSL", False)
    DEFAULT_MAIL_SENDER = env(
        "DEFAULT_MAIL_SENDER", "Flask BDA <me@example.com>"
    )

    ###############
    # File Upload #
    ###############
    UPLOAD_FOLDER = env("UPLOAD_FOLDER", "app/static/uploads")
    ALLOWED_EXTENSIONS = env(
        "ALLOWED_EXTENSIONS",
        set(
            [
                "txt",
                "rtf",
                "docx",
                "doc",
                "docm",
                "dotx",
                "odt",
                "xlsx",
                "xlsm",
                "xlsb",
                "xls",
                "xltx",
                "ods",
                "csv",
                "xml",
                "json",
                "pdf",
                "png",
                "jpg",
                "jpeg",
                "gif",
            ]
        ),
    )

    ###########
    # Swagger #
    ###########
    SWAGGER_BLUEPRINT_URL_PREFIX = env(
        "SWAGGER_BLUEPRINT_URL_PREFIX", "/swagger"
    )
    SWAGGER_URL = env(
        "SWAGGER_URL", "/api/docs"
    )  # URL for exposing Swagger UI (without trailing '/')
    SWAGGER_API_URL = env(
        "SWAGGER_API_URL", "swagger.json"
    )  # Our API url (can of course be a local resource)


class DevelopmentConfig(Config):
    def __init__(self, **kwargs: Any) -> None:
        config = {
            **dotenv_values(
                ".env.development",
            ),  # load development environment variables
            **kwargs,  # load passed in variables
            **os.environ,  # override loaded values with environment variables
        }
        super(Config, self).__init__(**config)
        self.__dict__.update(config)

    DEBUG = True
    DATABASE_URI = env("DATABASE_URI", DEV_DATABASE_URI)

    SQLALCHEMY_BINDS = {"default": DATABASE_URI}


class TestConfig(Config):
    def __init__(self, **kwargs: Any) -> None:
        config = {
            **dotenv_values(
                ".env.test",
            ),  # load test environment variables
            **kwargs,  # load passed in variables
            **os.environ,  # override loaded values with environment variables
        }
        super(Config, self).__init__(**config)
        self.__dict__.update(config)

    TESTING = True
    DATABASE_URI = env("DATABASE_URI", TEST_DATABASE_URI)

    SQLALCHEMY_BINDS = {"default": DATABASE_URI}


class ProductionConfig(Config):
    def __init__(self, **kwargs: Any) -> None:
        config = {
            **dotenv_values(
                ".env.production",
            ),  # load production environment variables
            **kwargs,  # load passed in variables
            **os.environ,  # override loaded values with environment variables
        }
        super(Config, self).__init__(**config)
        self.__dict__.update(config)

    DATABASE_URI = env("DATABASE_URI", PROD_DATABASE_URI)

    SQLALCHEMY_BINDS = {"default": DATABASE_URI}


default_config_factory: Dict[
    str, Union[Config, ProductionConfig, DevelopmentConfig, TestConfig]
] = {
    "default": Config,
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "testing": TestConfig,
}
