from titan.debug import Debugger
from titan.message import PiranhaMessage

class MessageManager:
    def __init__(self, connection):
        self.connection = connection

    async def receive_message(self, message: PiranhaMessage):
        Debugger.print(f"Received message of type: {message.get_message_type()}")

        match message.get_message_type():
            case _:
                ...