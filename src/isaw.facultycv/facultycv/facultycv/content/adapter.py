from plone.app.users.browser.personalpreferences import UserDataPanelAdapter

class FacultyCVUserPanelAdapter(UserDataPanelAdapter):
    """
    """

    def get_CVReference(self):
        return self.context.getProperty('CVReference', '')
    def set_CVReference(self, value):
        return self.context.setMemberProperties({'CVReference': value})
    CVReference = property(get_CVReference, set_CVReference)

