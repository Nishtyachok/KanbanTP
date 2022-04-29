
from .base import *

try:
    from .local import *
except ImportError:
    print('Cant find module settings.local! Make it from local.py.skeleton.')
