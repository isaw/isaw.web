from plone.app.registry.browser import controlpanel
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

from .interfaces import IISAWSettings


class ISAWSettingsEditForm(controlpanel.RegistryEditForm):

    schema = IISAWSettings
    label = "ISAW Settings"
    description = "Custom settings for ISAW web site."

    def updateFields(self):
        super(ISAWSettingsEditForm, self).updateFields()
        self.fields['emergency_message'].widgetFactory = WysiwygFieldWidget
        self.fields['footer_html'].widgetFactory = WysiwygFieldWidget


class ISAWSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = ISAWSettingsEditForm
