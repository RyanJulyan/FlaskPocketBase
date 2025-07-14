import sys, os
from dataclasses import dataclass
import secrets
from typing import Any, Dict, Union

import pprint
from dotenv import dotenv_values

from app.services.util.parse_yes_no_true import parse_yes_no_true
from app import __version__
from configuration.database_config import (
    DEFAULT_DATABASE_URI,
    DEV_DATABASE_URI,
    TEST_DATABASE_URI,
    PROD_DATABASE_URI,
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

        self.BASE_DIR = BASE_DIR

        ###########################
        # Development environment #
        ###########################
        self.DEBUG = env("DEBUG", False)
        self.DEBUG_TB_PROFILER_ENABLED = env(
            "DEBUG_TB_PROFILER_ENABLED", False
        )
        self.DEBUG_TB_INTERCEPT_REDIRECTS = env(
            "DEBUG_TB_INTERCEPT_REDIRECTS", False
        )
        self.TESTING = env("TESTING", False)

        ###################
        # List Formatting #
        ###################
        self.LIST_SEPARATOR = env("LIST_SEPARATOR", ",")
        self.CSV_DELIMITER = env("CSV_DELIMITER", "|")

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
        self.DATE_FORMAT = env("DATE_FORMAT", "%Y/%m/%d")
        self.TIME_FORMAT = env("TIME_FORMAT", "%H:%M:%S")
        self.DATETIME_FORMAT = env(
            "DATETIME_FORMAT", f"{self.DATE_FORMAT} {self.TIME_FORMAT}"
        )

        ###################################################
        # Manage SQLALCHEMY_ENGINE_OPTIONS like pool size #
        ###################################################
        # https://docs.sqlalchemy.org/en/13/core/engines.html#sqlalchemy.create_engine.params.pool_pre_ping
        # https://docs.sqlalchemy.org/en/13/core/engines.html#sqlalchemy.create_engine.params.pool_size
        # https://docs.sqlalchemy.org/en/13/core/engines.html#sqlalchemy.create_engine.params.pool_recycle
        self.SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_pre_ping": env("POOL_PRE_PING", True),
            "pool_recycle": env("POOL_RECYCLE", -1),
        }

        ################################################
        # Run create_database() in @app.before_request #
        ################################################
        self.AUTO_CREATE_DATABASE = env("AUTO_CREATE_DATABASE", True)

        ###########################################################
        # Run user_datastore.create_user() in @app.before_request #
        ###########################################################
        self.AUTO_CREATE_ADMIN_USER = env("AUTO_CREATE_ADMIN_USER", True)
        self.ADMIN_EMAIL = env("ADMIN_EMAIL", "admin")
        self.ADMIN_PASSWORD = env("ADMIN_PASSWORD", "admin")

        ##############################################
        # Run db.create_all() in @app.before_request #
        ##############################################
        self.AUTO_CREATE_TABLES_FROM_MODELS = env(
            "AUTO_CREATE_TABLES_FROM_MODELS", True
        )

        self.SQLALCHEMY_DATABASE_URI = env(
            "SQLALCHEMY_DATABASE_URI", DEFAULT_DATABASE_URI
        )

        self.SQLALCHEMY_BINDS = {"default": self.SQLALCHEMY_DATABASE_URI}

        self.SQLALCHEMY_TRACK_MODIFICATIONS = env(
            "SQLALCHEMY_TRACK_MODIFICATIONS", False
        )

        ########################
        # Application threads. #
        ########################
        self.THREADS_PER_PAGE = env("THREADS_PER_PAGE", 3)

        ############################
        # Time for session expirey #
        ############################
        self.TIME_TO_EXPIRE = env("TIME_TO_EXPIRE", 3600)

        ################################################################
        # Enable protection agains *Cross-site Request Forgery (CSRF)* #
        ################################################################
        self.CSRF_ENABLED = env("CSRF_ENABLED", True)
        self.CSRF_SESSION_KEY = env(
            "CSRF_SESSION_KEY", secrets.token_urlsafe(256)
        )

        #######################################################
        # Secret key for security, signing cookies and Tokens #
        #######################################################
        self.SECRET_KEY = env("SECRET_KEY", secrets.token_urlsafe(256))
        self.SECURITY_PASSWORD_LENGTH_MIN = env(
            "SECURITY_PASSWORD_LENGTH_MIN", 12
        )
        self.SECURITY_PASSWORD_SALT = env(
            "SECURITY_PASSWORD_SALT", secrets.token_urlsafe(256)
        )
        self.SECURITY_PASSWORD_HASH = env("SECURITY_PASSWORD_HASH", "argon2")
        self.SECURITY_REGISTERABLE = env("SECURITY_REGISTERABLE", True)
        self.SECURITY_PASSWORD_COMPLEXITY_CHECKER = env(
            "SECURITY_PASSWORD_COMPLEXITY_CHECKER", "zxcvbn"
        )

        ##################
        # flask_talisman #
        ##################
        """
        handles setting HTTP headers that can help protect against a few common web application security issues.
        blocks unauth images, scripts, styles, fonts, iframes, etc.
        allows traffic from our domain by default
        """
        self.CONTENT_SECURITY_POLICY = {
            "default-src": env("CSP_DEFAULT_SRC", "'self'"),
            "img-src": env("CSP_IMG_SRC", "* data:"),
            "connect-src": env("CSP_CONNECT_SRC", "'self'"),
            "media-src": env("CSP_MEDIA_SRC", "'self' blob:"),
            "script-src": env("CSP_SCRIPT_SRC", "'self'"),
            "style-src": env("CSP_STYLE_SRC", "'self' 'unsafe-inline'"),
            "font-src": env("CSP_FONT_SRC", "'self'"),
            "frame-src": env("CSP_FRAME_SRC", "'self'"),
            "child-src": env("CSP_CHILD_SRC", "'self'"),
            "media-src": env("CSP_MEDIA_SRC", "'self'"),
        }
        self.CONTENT_SECURITY_POLICY_REPORT_URI = env(
            "CONTENT_SECURITY_POLICY_REPORT_URI", None
        )
        self.SESSION_COOKIE_SECURE = parse_yes_no_true(
            env("SESSION_COOKIE_SECURE", "True")
        )
        self.SESSION_COOKIE_HTTPONLY = parse_yes_no_true(
            env("SESSION_COOKIE_HTTPONLY", "True")
        )
        self.SESSION_COOKIE_SAMESITE = env("SESSION_COOKIE_SAMESITE", "Lax")
        self.X_XSS_PROTECTION = parse_yes_no_true(
            env("X_XSS_PROTECTION", "True")
        )
        self.X_CONTENT_TYPE_OPTIONS = parse_yes_no_true(
            env("X_CONTENT_TYPE_OPTIONS", "True")
        )
        self.FRAME_OPTIONS = env("FRAME_OPTIONS", "DENY")
        self.FORCE_HTTPS = parse_yes_no_true(env("FORCE_HTTPS", "True"))
        self.STRICT_TRANSPORT_SECURITY = parse_yes_no_true(
            env("STRICT_TRANSPORT_SECURITY", "True")
        )
        self.STRICT_TRANSPORT_SECURITY_MAX_AGE = int(
            env("STRICT_TRANSPORT_SECURITY_MAX_AGE", 31536000)
        )
        self.STRICT_TRANSPORT_SECURITY_INCLUDE_SUBDOMAINS = parse_yes_no_true(
            env("STRICT_TRANSPORT_SECURITY_INCLUDE_SUBDOMAINS", "True")
        )

        ################################################
        # Secret key for signing JWT (JSON Web Tokens) #
        ################################################
        self.JWT_SECRET_KEY = env("JWT_SECRET_KEY", secrets.token_urlsafe(256))
        self.JWT_ACCESS_TOKEN_EXPIRES = env("JWT_ACCESS_TOKEN_EXPIRES", 3600)
        self.JWT_BLACKLIST_ENABLED = env("JWT_BLACKLIST_ENABLED", True)
        self.JWT_BLACKLIST_TOKEN_CHECKS = env(
            "JWT_BLACKLIST_TOKEN_CHECKS", ["access", "refresh"]
        )

        ########################
        # CORS ORIGINS allowed #
        ########################
        self.CORS_ORIGINS = env("CORS_ORIGINS", "*").split(",")
        self.CORS_RESOURCES = {
            r"/api/*": {"origins": env("CORS_ORIGINS", "*").split(",")}
        }
        self.CORS_SUPPORTS_CREDENTIALS = parse_yes_no_true(
            env("CORS_SUPPORTS_CREDENTIALS", "True")
        )
        self.CORS_ALLOW_HEADERS = env(
            "CORS_ALLOW_HEADERS", "Content-Type,Authorization"
        ).split(",")
        self.CORS_METHODS = env(
            "CORS_METHODS", "GET,POST,PUT,DELETE,OPTIONS"
        ).split(",")
        self.CORS_MAX_AGE = int(env("CORS_MAX_AGE", 86400))

        ##########################
        # flask_limiter for site #
        ##########################
        self.RATELIMIT_STORAGE_URI = env("RATELIMIT_STORAGE_URI", "memory://")
        self.RATELIMIT_DEFAULT = env(
            "RATELIMIT_DEFAULT",
            "10000/day;3000/hour;50/second",  # TODO: change the serve_file funtion to get all and send as one request
        )

        ##########################
        # flask_limiter for site #
        ##########################
        self.RATELIMIT_STORAGE_URI = env("RATELIMIT_STORAGE_URI", "memory://")
        self.RATELIMIT_DEFAULT = env(
            "RATELIMIT_DEFAULT",
            "10000/day;3000/hour;50/second",  # TODO: change the serve_file funtion to get all and send as one request
        )

        ###############
        # File Upload #
        ###############
        self.UPLOAD_FOLDER = env("UPLOAD_FOLDER", "app/static/uploads")
        self.ALLOWED_EXTENSIONS = env(
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

        #######
        # API #
        #######
        self.API_VERSION = env("API_VERSION", __version__.__version__)
        self.DEFAULT_AUTHORIZATIONS = {
            "jwt": {
                "type": env("JWT_AUTH_TYPE", "apiKey"),
                "in": env("JWT_AUTH_IN", "header"),
                "name": env("JWT_AUTH_NAME", "Authorization"),
            },
            "apikey": {
                "type": env("API_KEY_AUTH_TYPE", "apiKey"),
                "in": env("API_KEY_AUTH_IN", "header"),
                "name": env("API_KEY_AUTH_NAME", "ApiKey"),
            },
        }

        ###########
        # Swagger #
        ###########
        self.SWAGGER_BLUEPRINT_URL_PREFIX = env(
            "SWAGGER_BLUEPRINT_URL_PREFIX", "/swagger"
        )
        self.SWAGGER_URL = env(
            "SWAGGER_URL", "/api/docs"
        )  # URL for exposing Swagger UI (without trailing '/')
        self.SWAGGER_API_URL = env(
            "SWAGGER_API_URL", "swagger.json"
        )  # Our API url (can of course be a local resource)

        # Update from inputs or Environment Variables
        config = {
            **dotenv_values(
                "configuration/.env.shared",
            ),  # load shared environment variables
            **kwargs,  # load passed in variables
            **os.environ,  # override loaded values with environment variables
        }
        self.__dict__.update(config)


@dataclass
class DevelopmentConfig(Config):
    def __init__(self, **kwargs: Any) -> None:

        self.DEBUG = env("DEBUG", True)
        self.DEBUG_TB_PROFILER_ENABLED = env("DEBUG_TB_PROFILER_ENABLED", True)
        self.DEBUG_TB_INTERCEPT_REDIRECTS = env(
            "DEBUG_TB_INTERCEPT_REDIRECTS", True
        )
        self.SQLALCHEMY_DATABASE_URI = env(
            "SQLALCHEMY_DATABASE_URI", DEV_DATABASE_URI
        )

        self.SQLALCHEMY_BINDS = {"default": self.SQLALCHEMY_DATABASE_URI}

        # Update from inputs or Environment Variables
        config = {
            **dotenv_values(
                "configuration/.env.development",
            ),  # load development environment variables
            **kwargs,  # load passed in variables
            **os.environ,  # override loaded values with environment variables
        }
        super().__init__(**config)
        self.__dict__.update(config)


@dataclass
class TestConfig(Config):
    def __init__(self, **kwargs: Any) -> None:

        self.TESTING = env("TESTING", True)
        self.SQLALCHEMY_DATABASE_URI = env(
            "SQLALCHEMY_DATABASE_URI", TEST_DATABASE_URI
        )

        self.SQLALCHEMY_BINDS = {"default": self.SQLALCHEMY_DATABASE_URI}

        # Update from inputs or Environment Variables
        config = {
            **dotenv_values(
                "configuration/.env.test",
            ),  # load test environment variables
            **kwargs,  # load passed in variables
            **os.environ,  # override loaded values with environment variables
        }
        super().__init__(**config)
        self.__dict__.update(config)


@dataclass
class ProductionConfig(Config):
    def __init__(self, **kwargs: Any) -> None:

        self.SQLALCHEMY_DATABASE_URI = env(
            "SQLALCHEMY_DATABASE_URI", PROD_DATABASE_URI
        )

        self.SQLALCHEMY_BINDS = {"default": self.SQLALCHEMY_DATABASE_URI}

        # Update from inputs or Environment Variables
        config = {
            **dotenv_values(
                "configuration/.env.production",
            ),  # load production environment variables
            **kwargs,  # load passed in variables
            **os.environ,  # override loaded values with environment variables
        }
        super().__init__(**config)
        self.__dict__.update(config)


default_config_factory: Dict[
    str, Union[Config, ProductionConfig, DevelopmentConfig, TestConfig]
] = {
    "default": Config,
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "test": TestConfig,
}


if __name__ == "__main__":
    config_name = "development"
    config = default_config_factory[config_name]()
    pprint.pprint(config.__dict__)
