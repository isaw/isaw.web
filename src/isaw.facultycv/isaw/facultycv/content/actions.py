from Products.CMFCore.utils import getToolByName


def initial_setup(obj, event):
    memberdata = getToolByName(obj, "portal_memberdata")
    membertool = getToolByName(obj, "portal_membership")

    # Create profile for initial CV
    obj.invokeFactory("CV", id="cv", title="Curriculum Vitae")

    # Set the reference of profile to the CV
    cv = obj['cv']
    uid = cv.UID()
    obj.setProfileRef(uid)

    # Set the reference of the member to the CV
    if not memberdata.hasProperty("CVReference"):
        memberdata.manage_addProperty(id="CVReference", value="", type="string")
    obj.setProfileRef(uid)
    uri = obj.absolute_url()

    # Turn on permissions for membertool
    obj.manage_permission(
        "Manage users",
        roles=['Manager', 'Authenticated', 'Owner'],
        acquire=1
    )
    member = membertool.getAuthenticatedMember()
    member.setMemberProperties(mapping={"CVReference": uri})

    # Turn off permissions for membertool
    obj.manage_permission(
        "Manage users",
        roles=['Manager', 'Authenticated', 'Owner'],
        acquire=0)

    # set profile UID on corresponding member:
    memberID = obj.getMemberID()
    if memberID:
        linked_member = membertool.getMemberById(memberID)

    if linked_member is not None:
        linked_member.setMemberProperties({'ProfileReference': obj.UID()})


def profile_updated(obj, event):
    """When a Profile is updated, check for a MemberID value.
       If it's set, find the corresponding Plone member and update their
       ProfileReference property, to maintain a bidirectional mapping
       between members and their Profiles.
    """
    membertool = getToolByName(obj, "portal_membership")
    memberID = obj.getMemberID()
    if memberID:
        member = membertool.getMemberById(memberID)
        if member is not None:
            member.setMemberProperties({'ProfileReference': obj.UID()})
        return
    # We may have *removed* a user ID, and we don't have access to the value
    # previously set, so we have to look at all the members:
    for member in membertool.listMembers():
        if member.getProperty('ProfileReference') == obj.UID():
            member.setMemberProperties({'ProfileReference': ''})
            break
