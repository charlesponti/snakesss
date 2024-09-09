from typing import List

import strawberry
from strawberry.file_uploads import Upload

from lib.images import ImageResolver

from src.schemas.types import Message, Note


def send_chat_message():
    return []


async def upload_voice_note(self, info: strawberry.Info, audio_file: Upload, chat_id: int) -> List[Note]:
    return []


@strawberry.type
class Mutation:
    # Media
    save_image_info: bool = strawberry.field(resolver=ImageResolver.save_image_info)

    # Chat
    send_chat_message: List[Message] = strawberry.field(resolver=send_chat_message)

    # Notes
    upload_voice_note: List[Note] = strawberry.field(resolver=upload_voice_note)
