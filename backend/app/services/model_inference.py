from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

def load_qwen_generator():
    model_id = "Qwen/Qwen3-4B-Instruct-2507" 
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id, 
        torch_dtype="auto", 
        low_cpu_mem_usage=True, 
        device_map="auto"
    ) 

    generator = pipeline(
        task="text-generation",
        model=model,
        tokenizer=tokenizer,
        return_full_text=False, # Don't want to include prompt in response
        max_new_tokens=256,
        do_sample=True, 
        temperature=0.7,
        top_p=0.9
    )

    return generator