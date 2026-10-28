import json
from pathlib import Path
from fastapi import APIRouter, Depends

from app.api.dependencies import get_conversation_path, get_generator
from app.schemas.model_inference import ModelInferenceRequest, ModelInferenceResponse

router = APIRouter(prefix="/gentext")


@router.post("/qweninference", response_model=ModelInferenceResponse)
def qwen_inference(
    request: ModelInferenceRequest,
    generator=Depends(get_generator),
    conversation_path: Path = Depends(get_conversation_path),
):
    with open(conversation_path, "r") as file:
        messages = json.load(file)

    user_message = {"role": "user", "content": request.prompt}
    messages.append(user_message)

    output = generator(messages)
    model_response = output[0]['generated_text']

    model_message = {"role": "assistant", "content": model_response}
    messages.append(model_message)

    with open(conversation_path, "w") as file:
        json.dump(messages, file, indent=2)

    return {
        "model_response": model_response,
        "char_count": len(model_response)
    }