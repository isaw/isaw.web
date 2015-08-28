from zope.interface import Interface
from zope import schema
from zope.viewlet.interfaces import IViewletManager

from plone.theme.interfaces import IDefaultPloneLayer


class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """


class ILeftCol(IViewletManager):
    """A viewlet manager that sits in the left most column of the page
       (an addition to the main template)
    """


class IUtilsView(Interface):
    """ Marker interface for misc browser view """

    def getUpcomingEvents(limit):
        """Grabbing upcoming events for the home page"""

    def getMonthName(self, month):
        """ Translates a month int into a short name """

    def formatSiteMap(self, code):
        """ Customizes the sitemap pre-formated code to fit the comps """


class ITiledListingView(Interface):
    """marker interface for a view providing tiled view listed items

    This view is suitable for folders or collections
    """


class IEventListingView(Interface):
    """marker interface for a view providing one column listed items

    This view is suitable for folders or collections
    """


DEFAULT_FOOTER_HTML = u"""<div class="contact footer-portlet">
<h3>Contact</h3>
<p>15 East 84th St.<br>New York, NY 10028<br>212-992-7800<br>
<a href="mailto:isaw@nyu.edu">isaw@nyu.edu</a></p>
</div>
<div id="footer-support" class="support footer-portlet">
<h3 class="support">
<a href="http://isaw4-dev.atlantides.org/support-isaw">Support ISAW</a></h3>
<ul><li id="personaltools-login">
<a href="https://isaw.nyu.edu/Shibboleth.sso/login?target=https://isaw.nyu.edu/isaw-home">Log in</a>
</li><li id="personaltools-support">
<a href="http://isaw4-dev.atlantides.org/support-isaw">Support ISAW</a>
</li><li id="personaltools-careers">
<a href="http://isaw4-dev.atlantides.org/jobs">Careers at ISAW</a>
</li><li id="personaltools-newsrss">
<a href="http://isaw4-dev.atlantides.org/news/RSS">News RSS</a>
</li></ul>
</div>
<div class="hours footer-portlet">
<h3>Gallery Hours</h3>
<p>The galleries are currently closed.</p>
</div>
<div class="hours footer-portlet">
<h3>Library Hours</h3>
<p><strong>Mon-Fri</strong> 9am-5pm</p>
</div>"""

class IISAWSettings(Interface):
    emergency_message = schema.Text(title=u"Emergency Message",
            description=u"Any text here will be displayed at the top of the site. An empty field means do not display emergency message",
            required=False)
    footer_html = schema.Text(title=u"Footer HTML",
            description=u"The full HTML of the site footer",
            required=True,
            default=DEFAULT_FOOTER_HTML)
