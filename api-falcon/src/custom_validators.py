import re
from graceful.errors import ValidationError


def is_valid_sorting(value):
    VALID_FIELDS = [
        "descriptor.first_obligation",
        "descriptor.total_obligation",
        "descriptor.duration",
        "descriptor.interest_rate",
        "descriptor.punitive_interest_rate",
        "descriptor.frequency",
        "descriptor.installments",

        "expiration",
        "amount",
        "created",
        "currency"
    ]

    if not value["field"] in VALID_FIELDS:
        raise ValidationError("{} is not a valid field".format(value["field"]))
