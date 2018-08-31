from .patches import allow_not_uuid
from .patches import img_tag_no_title


def initialize(context):
    allow_not_uuid()
    img_tag_no_title()
