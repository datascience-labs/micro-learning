from pydantic import BaseModel
from typing import List

class MicroLearningSequence(BaseModel):
    id: str
    title: str
    segment_ids: List[str]
    cognitive_level: str
    dok_level: str
