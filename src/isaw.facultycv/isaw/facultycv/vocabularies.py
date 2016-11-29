from Products.CMFCore.utils import getToolByName
from zope.interface import directlyProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary


def UsersVocabularyFactory(context):

    acl_users = getToolByName(context, 'acl_users')
    terms = [(SimpleVocabulary.createTerm('', '', 'None'))]

    for user in acl_users.getUsers():
        if user is not None:
            member_id = user.getId()
            member_name = user.getProperty('fullname') or user.getId()
            terms.append(SimpleVocabulary.createTerm(
                user.getId(),
                str(member_id),
                member_name)
            )

    return SimpleVocabulary(terms)

directlyProvides(UsersVocabularyFactory, IVocabularyFactory)
