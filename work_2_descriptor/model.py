import json


class Model:

    def __init__(self, path):
        self.path = path

        try:
            with open(self.path, 'r', encoding='UTF-8') as f:
                self.data = json.load(f)
        except json.decoder.JSONDecodeError:
            self.data = {}

    def save(self):
        with open(self.path, 'w', encoding='UTF-8') as f:
            json.dump(self.data, f)


class Field:

    def __init__(self, name):
        self.name = name

    def __set__(self, instance, value):
        instance.data[self.name] = value
        instance.save()

    def __get__(self, instance, owner):
        with open(instance.path, 'r', encoding='UTF-8') as f:
            data = json.load(f)
            return data.get(self.name)

    def __delete__(self, instance):
        with open(instance.path, 'r+', encoding='UTF-8') as f:
            data = json.load(f)
            if self.name in data:
                del data[self.name]
            f.seek(0)
            f.truncate()
            instance.data = data
            json.dump(data, f)
