from enum import Enum
from typing import List, Optional
import strawberry


@strawberry.enum
class MessageRole(Enum):
    USER = "user"
    ASSISTANT = "assistant"


@strawberry.type
class Profile:
    id: int
    name: str | None
    avatar_url: str | None
    user_id: str


@strawberry.type
class Chat:
    id: int
    title: str
    created_at: str
    user_id: str


@strawberry.type
class Message:
    id: int
    content: str
    created_at: str
    user_id: str
    chat_id: int
    role: MessageRole


@strawberry.type
class ChatMessageInput:
    chat_id: int
    message: str


@strawberry.type
class ChatMessageOutput:
    content: str


@strawberry.type
class Notebook:
    title: str
    id: str
    created_at: str
    updated_at: str
    user_id: str


@strawberry.type
class Note:
    content: str
    id: str
    created_at: str
    user_id: str


@strawberry.type
class User:
    id: str
    email: str | None


# Enums
@strawberry.enum
class MediaTypeValue(Enum):
    PHOTO = "photo"
    VIDEO = "video"
    AUDIO = "audio"


@strawberry.enum
class MediaSubtype(Enum):
    DEPTH_EFFECT = "depthEffect"
    HDR = "hdr"
    HIGH_FRAME_RATE = "highFrameRate"
    LIVE_PHOTO = "livePhoto"
    PANORAMA = "panorama"
    SCREENSHOT = "screenshot"
    STREAM = "stream"
    TIMELAPSE = "timelapse"


# Types
@strawberry.type
class Location:
    latitude: float
    longitude: float


@strawberry.input
class Metadata:
    albumId: Optional[str] = None
    # creationTime: float
    # duration: float
    # filename: str
    # height: int
    # id: str
    # mediaSubtypes: Optional[List[MediaSubtype]] = None
    # isDepthPhoto: bool
    # isHDR: bool
    # isHighFrameRate: bool
    # isLivePhoto: bool
    # isPanorama: bool
    # isScreenshot: bool
    # isStream: bool
    # isTimeLapse: bool
    # mediaType: MediaTypeValue
    # modificationTime: float
    # uri: str
    # width: int
    # exif: Optional[dict] = None
    # isFavorite: Optional[bool] = None
    # isNetworkAsset: Optional[bool] = None
    # location: Optional[Location] = None
    # orientation: Optional[int] = None


@strawberry.type
class ImageInfo:
    id: str
    metadata: Metadata
    similarity: float


# Input types
@strawberry.input
class LocationInput:
    latitude: float
    longitude: float
