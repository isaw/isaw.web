import logging


logger = logging.getLogger('isaw.register')


def uninstall(portal, reinstall=False):
    if not reinstall:
        setup_tool = portal.portal_setup
        setup_tool.runAllImportStepsFromProfile('profile-isaw.register:uninstall')
        logger.info("Uninstall done")
