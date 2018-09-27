"""Global configuration and constants.
"""
import os

PROD_FLAG = 'ISAW_PRODUCTION'
IS_PRODUCTION = PROD_FLAG in os.environ and os.environ[PROD_FLAG] == 'True'
