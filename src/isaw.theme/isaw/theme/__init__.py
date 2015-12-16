from .patches import allow_not_uuid


def initialize(context):
    allow_not_uuid()
