"""Global configuration and constants.
"""
import os

PROD_FLAG = 'ISAW_PRODUCTION'
IS_PRODUCTION = PROD_FLAG in os.environ and os.environ[PROD_FLAG] == 'True'
# These paths are relative to CLIENT_HOME (ie, buildout_root/parts/clientX/)
SAML_CERT_PATH = '../../conf/isaw-{}.der'.format(
    'production' if IS_PRODUCTION else 'staging'
)
SAML_PRIVATE_KEY_PATH = '../../conf/isaw-{}.pem'.format(
    'production' if IS_PRODUCTION else 'staging'
)
