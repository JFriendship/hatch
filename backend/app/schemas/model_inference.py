from pydantic import BaseModel, Field

class ModelInferenceRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=2000)

class ModelInferenceResponse(BaseModel):
    model_response: str
    char_count: int