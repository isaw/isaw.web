from zope.component import queryUtility

from plone.registry.interfaces import IRegistry
from plone.app.theming.interfaces import IThemeSettings


class ThemeSettingsView(object):
    """Returns info about theme settings, this is to workaround the
    fact that plone.app.theming does not have a reliable way to
    determine if a site is themed."""

    def _get_settings(self):
        registry = queryUtility(IRegistry)
        if registry is None:
            return None

        try:
            settings = registry.forInterface(IThemeSettings)
        except KeyError:
            return None

        return settings

    def theme_blacklist(self):
        """Returns the list of theme blacklisted hosts"""
        settings = self._get_settings()
        return dict((h,1) for h in settings.hostnameBlacklist or ())

    def is_blacklisted(self):
        """Is the current host a blacklisted host"""
        blacklist = self.theme_blacklist()

        base = self.request.get('BASE1')
        _, base = base.split('://', 1)
        host = base.lower()
        server_port = self.request.get('SERVER_PORT')

        if host in blacklist or host.replace(':'+server_port,'') in blacklist:
            return True
        else:
            return False

    def is_themed(self):
        """Returns true if a theme is applied"""
        if (self.request.get('HTTP_X_THEME_ENABLED') and
            not self.is_blacklisted()):
            return True
        else:
            return False
