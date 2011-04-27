from Products.CMFCore.utils import getToolByName
from zope.component import getUtility, getMultiAdapter
from zope.app.container.interfaces import INameChooser
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from collective.portlet.relateditems import relateditems


def initial_setup(obj, event):
    # Create profile for initial CV
    obj.invokeFactory("CV", id="cv", title="Curriculum Vitae")

    # Set the reference of profile to the CV
    print "Setting reference to CV" 
    cv = obj['cv']
    uid = cv.UID()
    print "UID OF profile folder " + uid
    obj.setProfileRef(uid)

    # Set the reference of the member to the CV
    print "Setting reference to member"
    memberdata = getToolByName(obj, "portal_memberdata")
    membertool = getToolByName(obj, "portal_membership")

    if not memberdata.hasProperty("CVReference"):
        memberdata.manage_addProperty(id="CVReference", value="", type="string")

    obj.setProfileRef(uid)
    uri = obj.absolute_url()
    # Turn on permissions for membertool
    obj.manage_permission("Manage users", roles=['Manager', 'Authenticated', 'Owner'], acquire = 1)
    member = membertool.getAuthenticatedMember()
    member.setMemberProperties(mapping={"CVReference": uri})
    # Turn off permissions for membertool
    obj.manage_permission("Manage users", roles=['Manager', 'Authenticated', 'Owner'], acquire = 0)

    # The below is commented out because the related portlet addon
    # isn't what was required by the client.

    # Assigned related portlet to Profile
    #column = getUtility(IPortletManager, name='plone.rightcolumn')                                                      
    #manager = getMultiAdapter((obj, column,), IPortletAssignmentMapping)
    #assignment = relateditems.Assignment(
    #    count = 5,
    #    states=('published',),
    #    allowed_types= ('Profile',)
    #)
    #chooser = INameChooser(manager)
    #manager[chooser.chooseName(None, assignment)] = assignment

