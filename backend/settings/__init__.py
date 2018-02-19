from backend.settings.base import *

try:
    from backend.settings.local import *
except ImportError as e:
    # No local settings file found.
    # You can still override using environment variables.
    pass
