from graceful.fields import BaseField

class ListField(BaseField):
    def __init__(self, details, serializer=None, **kwargs):
        super().__init__(details, **kwargs)
        self._serializer = serializer

    type = "list"

    def from_representation(self, data):
        raise NotImplementedError()

    def to_representation(self, value):
        return [self._serializer.to_representation(obj) for obj in value]
