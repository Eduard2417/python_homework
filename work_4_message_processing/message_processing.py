from enum import Enum, auto


class MessageType(Enum):
    TELEGRAM = auto()
    MATTERMOST = auto()
    SLACK = auto()


class JsonMessage:
    def __init__(self, message_type: MessageType, payload: str):
        self.message_type = message_type
        self.payload = payload


class ParseFactory:
    def __init__(self):
        self.data = {}

    def add_message(self, message: MessageType):
        def wrapper(cls):
            self.data[message] = cls(message)
            return cls(message)
        return wrapper

    def get(self, message_type):
        return self.data[message_type]


factory = ParseFactory()


class MessageParser:
    def __init__(self, message):
        self.message = message

    def parse(self):
        pass


@factory.add_message(message=MessageType.TELEGRAM)
class TelegramMessage(MessageParser):

    def parse(self):
        print('парсер для телеграма')


@factory.add_message(message=MessageType.MATTERMOST)
class MattermostMessage(MessageParser):

    def parse(self):
        print('парсер для метт')


@factory.add_message(message=MessageType.SLACK)
class SlackMessage(MessageParser):

    def parse(self):
        print('парсер для слек')
