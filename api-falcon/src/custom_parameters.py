import re
from graceful.parameters import BaseParam

class SortingParam(BaseParam):
    """ Represents a search parameter in string form of "field__[asc|desc]"
    """
    type = 'sorting'

    def value(self, raw_value):
        re_field = re.compile("^(?P<field>[a-zA-Z._]+)__(?P<type>asc|desc)$")
        fields = re_field.match(raw_value).groupdict()

        return fields