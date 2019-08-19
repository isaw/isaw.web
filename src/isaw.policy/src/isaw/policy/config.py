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

SSO_PLUGIN_ID = 'saml2sp'

if IS_PRODUCTION:
    SAML_IDENTITY_PROVDER_URL = 'http://shibboleth.nyu.edu/idp/shibboleth'
    SAML_IDENTITY_PROVDER_TITLE = 'NYI Production SSO Identity Provider Entity'
else:
    SAML_IDENTITY_PROVDER_URL = 'https://shibbolethqa.es.its.nyu.edu/idp/shibboleth'
    SAML_IDENTITY_PROVDER_TITLE = 'NYI Staging/QA SSO Identity Provider Entity'
