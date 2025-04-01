from pydantic import BaseModel
from typing import Optional

class Playlist(BaseModel):
    id: str
    title: str
    description: Optional[str]
    channel_id: str
