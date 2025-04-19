from pydantic import BaseModel
from typing import List

class Sequence(BaseModel):
    id: str
    title: str
    segment_ids: List[str]
    cognitive_level: str
    dok_level: str
