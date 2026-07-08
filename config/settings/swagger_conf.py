# By Default swagger ui is available only to admin user(s). You can change permission classes to change that
# See more configuration options at https://drf-spectacular.readthedocs.io/en/latest/settings.html#settings
SPECTACULAR_SETTINGS = {
    "TITLE": "Project API",
    "DESCRIPTION": "{Name} of API endpoints of Project",
    "VERSION": "1.0.0",
    "SERVE_PERMISSIONS": ["rest_framework.permissions.IsAdminUser"],
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
    },
    "COMPONENT_SPLIT_REQUEST": True,
    "DISABLE_ERRORS_AND_WARNINGS": False,
    "EXTERNAL_DOCS": {
        "description": "Project Repository",
        "url": "https://github.com/username/project",
    },
    "CONTACT": {
        "name": "Your Name",
        "url": "FirDavsDev",
        "email": "email@gmail.com",
    },
    "LICENSE": {
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    "TAGS_SORTER": "alpha",
    "OPERATION_SORTER": "alpha",
    "JSON_EDITOR": True,
    "SWAGGER_UI": True,
    "REDOC": False,
    "DEFAULT_AUTO_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]",
    "SERVE_URLCONF": "config.urls",
    "SERVE_INCLUDE_SCHEMA": False,
    "SERVE_PUBLIC": False,
    "VALIDATOR_URL": None,
    "SWAGGER_UI_FAVICON_HREF": None,
    "SWAGGER_UI_LOGO_HREF": None,
    "SWAGGER_UI_EXTERNAL_CSS": None,
    # patterns to ignore in schema generation
    "IGNORED_PATHS": [
        r"^admin/panel/",
        r"^api-auth/",
        r"^api/token/",
        r"^api/token/refresh/",
        r"^api/token/verify/",
    ],
}
