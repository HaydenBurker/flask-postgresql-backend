import uuid

from util.records import serialize

class Model:
    primary_key = None
    tablename = None
    fields = []

    def set_fields(self):
        cls = type(self)
        if not cls.fields:
            cls.fields = list(self.__dict__.keys())

    def load(self, data):
        if type(data) == dict:
            fields = data.keys()
            self_fields = set(self.fields)

            for field in fields:
                if field in self_fields:
                    setattr(self, field, data[field])

        elif type(data) in [tuple, list]:
            keys = self.fields

            for i in range(len(keys)):
                setattr(self, keys[i], data[i])

        return self

    @classmethod
    def load_many(cls, data):
        return [cls().load(record) for record in data]

    def dump(self):
        return {k: serialize(v) for k, v in self.__dict__.items() if k in self.fields}

    def generate_key(self):
        setattr(self, self.primary_key, str(uuid.uuid4()))

    def dump_update(self):
        return {k: v for k, v in self.__dict__.items() if k in self.fields}
