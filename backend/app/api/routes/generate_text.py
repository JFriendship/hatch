from fastapi import APIRouter, Depends, Request

from app.api.dependencies import get_generator
from app.schemas.model_inference import ModelInferenceRequest, ModelInferenceResponse

router = APIRouter(prefix="/gentext")

@router.post("/qweninference", response_model=ModelInferenceResponse)
def qwen_inference(request: ModelInferenceRequest, generator=Depends(get_generator)):
    output = generator(request.prompt)
    model_response = output[0]['generated_text']

    return {
        "model_response": model_response,
        "char_count": len(model_response)
    }