from .base import *

DEBUG = False

STATICFILES_DIRS = [
    os.path.join(ROOT_DIR, "assets"),
]

WEBPACK_LOADER = {
    'DEFAULT': {
            'BUNDLE_DIR_NAME': 'bundles/',
            'STATS_FILE': os.path.join(ROOT_DIR, 'webpack-stats.prod.json'),
        }
}
