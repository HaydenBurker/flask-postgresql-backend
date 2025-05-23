import uuid

from util.records import serialize

class Model:
    primary_key = None
    tablename = None

    def load(self, data):
        if type(data) == dict:
            fields = data.keys()

            for field in fields:
                if hasattr(self, field):
                    setattr(self, field, data[field])

        elif type(data) in [tuple, list]:
            keys = list(self.__dict__.keys())

            for i in range(len(self.__dict__)):
                setattr(self, keys[i], data[i])

    def dump(self):
        return {k: serialize(v) for k, v in self.__dict__.items()}

    def generate_key(self):
        setattr(self, self.primary_key, str(uuid.uuid4()))

    def get_fields(self):
        return self.__dict__.keys()

    def dump_values(self):
        return [serialize(v) for v in self.__dict__.values()]
