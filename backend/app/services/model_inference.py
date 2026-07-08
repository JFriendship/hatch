import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

def get_device() -> str:
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    return device

def load_qwen_generator():
    device = get_device()

    model_id = "Qwen/Qwen2.5-3B" 
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id).to(device) # type: ignore

    generator = pipeline(
        task="text-generation",
        model=model,
        tokenizer=tokenizer,
        return_full_text=False, # Asking to include prompt in response
        max_new_tokens=100,
        do_sample=False # Always the same output. Equivalent to temperature=0
    )

    return generator