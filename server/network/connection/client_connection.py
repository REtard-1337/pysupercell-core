import asyncio

from server.network.protocol import MessageManager
from server.network.protocol import Messaging
from titan.debug.debugger import Debugger
from titan.message.piranha_message import PiranhaMessage


class ClientConnection:
    def __init__(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        self.reader = reader
        self.writer = writer
        self.messaging = Messaging(reader, writer, MessageManager(self))
        self.buffer = bytearray(8192)

    async def receive(self):
        try:
            offset = 0
            while True:
                data = await self.reader.read(4096)
                if not data:
                    break

                self.buffer[offset : offset + len(data)] = data
                offset += len(data)

                processed_offset = 0
                while True:
                    consumed = await self.messaging.on_receive(
                        self.buffer[processed_offset:offset], offset - processed_offset
                    )
                    if consumed == 0:
                        break
                    processed_offset += consumed

                if processed_offset > 0:
                    self.buffer[: offset - processed_offset] = self.buffer[
                        processed_offset:offset
                    ]
                    offset -= processed_offset

        except asyncio.CancelledError:
            pass
        except Exception as ex:
            Debugger.error(f"Unhandled exception in session: {ex}")

    async def send_message(self, message: PiranhaMessage):
        await self.messaging.send(message)
