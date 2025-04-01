from pydantic import BaseModel
from typing import Optional

class Channel(BaseModel):
    id: str
    title: str
    description: Optional[str]
    published_at: Optional[str]
