import json

from decimal import Decimal

from .exceptions import SerializationError


class ServantJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if hasattr(obj, 'to_primitive'):
            return obj.to_primitive()

        if isinstance(obj, Decimal):
            return float(obj)

        return json.JSONEncoder.default(self, obj)


class JsonSerializer(object):

    def serialize(self, data):
        return json.dumps(data, cls=ServantJsonEncoder)

    def deserialize(self, data):
        try:
            return json.loads(data)
        except ValueError, err:
            raise SerializationError(err.message)
