from Products.PluginIndexes.UUIDIndex.UUIDIndex import UUIDIndex


def allow_not_uuid():
    UUIDIndex.query_options = tuple(UUIDIndex.query_options) + ('not',)
