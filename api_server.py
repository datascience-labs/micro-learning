from fastapi import FastAPI
from pydantic import BaseModel
from controllers.video_segmentation_controller import segment_video_by_description
from controllers.microlearning_recommender import recommend_sequences_from_segments

app = FastAPI()

class VideoInput(BaseModel):
    video_id: str
    description: str

@app.post("/recommend")
def recommend_sequences(input_data: VideoInput):
    segments = segment_video_by_description(input_data.video_id, input_data.description)
    sequences = recommend_sequences_from_segments(segments)
    return {"sequences": [s.dict() for s in sequences]}
