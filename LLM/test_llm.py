
import torch
from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM, AutoTokenizer
import os
import sys
import psutil
import time

# Paths
BASE_MODEL_ID = "mistralai/Mistral-7B-v0.1"
ADAPTER_PATH = r"d:\Perosnal Projects\LAWKEASH\LLM\mistral-7b-indian-law-lora"

def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  # MB

def main():
    print(f"[{time.strftime('%H:%M:%S')}] Checking system resources...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device found: {device}")
    
    total_ram = psutil.virtual_memory().total / (1024 ** 3)
    available_ram = psutil.virtual_memory().available / (1024 ** 3)
    print(f"Total RAM: {total_ram:.2f} GB")
    print(f"Available RAM: {available_ram:.2f} GB")
    
    if device == "cpu":
        print("WARNING: Running on CPU.")
        if available_ram < 16:
            print("CRITICAL WARNING: Less than 16GB RAM available. Model loading will likely crash or freeze.")
    
    print(f"[{time.strftime('%H:%M:%S')}] Loading base model: {BASE_MODEL_ID}")
    
    # Load Tokenizer
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_ID, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    
    # On CPU, float32 is safer but huge. float16 is smaller but might be unsupported on some ops.
    # We'll try float16 to save memory, if it fails, user might need more RAM for float32.
    dtype_to_use = torch.float32 if device == "cpu" else torch.float16
    print(f"Using dtype: {dtype_to_use}")

    try:
        model = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL_ID,
            device_map=device,
            torch_dtype=dtype_to_use,
            trust_remote_code=True,
            low_cpu_mem_usage=True
        )
    except Exception as e:
        print(f"Error loading base model: {e}")
        sys.exit(1)
        
    print(f"[{time.strftime('%H:%M:%S')}] Base model loaded. Memory used: {get_memory_usage():.2f} MB")
    
    print(f"Loading LoRA adapter from: {ADAPTER_PATH}")
    try:
        model = PeftModel.from_pretrained(model, ADAPTER_PATH)
    except Exception as e:
        print(f"Error loading adapter: {e}")
        sys.exit(1)
            
    print(f"[{time.strftime('%H:%M:%S')}] Full model ready!")
    print("-" * 50)

    # Test Queries
    questions = [
        "What is the punishment for murder in India?",
        "Explain the rights of an arrested person.",
    ]
    
    for q in questions:
        print(f"\nQuery: {q}")
        prompt = f"Question: {q}\nAnswer:"
        
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        
        print("Generating response...")
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=100,
                temperature=0.7,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )
            
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"Result:\n{response}")
        print("-" * 50)

if __name__ == "__main__":
    main()
