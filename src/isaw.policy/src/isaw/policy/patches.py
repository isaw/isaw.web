# Miscellaneous monkey-patches
import logging
from Products.CMFCore.utils import getToolByName

logger = logging.getLogger(__name__)


def patch_saml_login():
    from dm.zope.saml2.spsso.plugin import IntegratedSimpleSpssoPlugin

    def authenticateCredentials(self, credentials):
        result = super(
            IntegratedSimpleSpssoPlugin, self
        ).authenticateCredentials(credentials)
        if not result or len(result) != 2:
            return result
        userid, login = result
        if userid == login:
            try:
                acl = getToolByName(self, 'acl_users')
            except (AttributeError, KeyError):
                acl = None
            if acl is None:
                return userid, login

            userids = [
                user.get('userid') for user in
                acl.searchUsers(name=login, exact_match=True)
                if user.get('userid')
            ]
        if len(userids) == 1:
            userid = userids[0]
        elif len(userids) > 1:
            logger.info('Too many matching userids found for login '
                        '{}, falling back to default'.format(login))
        elif len(userids) > 1:
            logger.info('No matching userids found for login '
                        '{}, falling back to default'.format(login))
        return userid, login
