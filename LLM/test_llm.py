
import torch
from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM, AutoTokenizer
import os

# Paths
BASE_MODEL_ID = "mistralai/Mistral-7B-v0.1"
ADAPTER_PATH = r"d:\Perosnal Projects\LAWKEASH\LLM\mistral-7b-indian-law-lora"

def main():
    print(f"Loading base model: {BASE_MODEL_ID}")
    
    # quantization_config = BitsAndBytesConfig(load_in_4bit=True, ...) # Optional if needed for memory
    
    # Load Tokenizer
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_ID, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    
    # Load Base Model
    # device_map="auto" will use GPU if available
    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL_ID,
        device_map="auto",
        torch_dtype=torch.float16,
        trust_remote_code=True
    )
    
    print(f"Loading LoRA adapter from: {ADAPTER_PATH}")
    model = PeftModel.from_pretrained(model, ADAPTER_PATH)
    
    print("Model loaded successfully!")
    print("-" * 50)

    # Test Queries
    questions = [
        "What is the punishment for murder in India?",
        "Explain the rights of an arrested person.",
        "What is the difference between culpable homicide and murder?"
    ]
    
    for q in questions:
        print(f"\nQuery: {q}")
        
        # Format prompt (Alpaca style or similar is common for instruction tuning, 
        # but straight text is fine for base check)
        # If the model was trained with a specific template, we should use it.
        # Assuming standard text generation for now.
        prompt = f"Question: {q}\nAnswer:"
        
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=200,
                temperature=0.7,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )
            
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Extract just the new part if possible, or print whole thing
        print(f"Result:\n{response}")
        print("-" * 50)

if __name__ == "__main__":
    main()
