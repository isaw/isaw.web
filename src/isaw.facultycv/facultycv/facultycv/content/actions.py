from Products.CMFCore.utils import getToolByName

def initial_setup(obj, event):
    # Create profile for initial CV
    obj.invokeFactory("profile", id="profile", title="profile")

    # Set the reference of profile to the CV
    print "Setting reference to profile" 
    profile = obj['profile']
    uid = profile.UID()
    print "UID OF profile folder " + uid
    obj.setProfileRef(uid)

    # Set the reference of the member to the CV
    print "Setting reference to member"
    memberdata = getToolByName(obj, "portal_memberdata")
    membertool = getToolByName(obj, "portal_membership")

    if not memberdata.hasProperty("CVReference"):
        memberdata.manage_addProperty(id="CVReference", value="", type="string")

    obj.setMemberRef(uid)
    uri = obj.absolute_url()
    # Turn on permissions for membertool
    obj.manage_permission("Manage users", roles=['Manager', 'Authenticated', 'Owner'], acquire = 1)
    member = membertool.getAuthenticatedMember()
    member.setMemberProperties(mapping={"CVReference": uri})
    # Turn off permissions for membertool
    obj.manage_permission("Manage users", roles=['Manager', 'Authenticated', 'Owner'], acquire = 0)


