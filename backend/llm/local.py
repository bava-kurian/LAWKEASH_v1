
import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import os
import sys

# Paths - Adjust if necessary
BASE_MODEL_ID = "mistralai/Mistral-7B-v0.1"
ADAPTER_PATH = r"d:\Perosnal Projects\LAWKEASH\LLM\mistral-7b-indian-law-lora"

class LocalLLM:
    _instance = None
    model = None
    tokenizer = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = LocalLLM()
        return cls._instance

    def __init__(self):
        if self.model is None:
            self._load_model()

    def _load_model(self):
        print("Loading Local LLM... This may take time.")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        try:
             # Load Tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_ID, trust_remote_code=True)
            self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Smart loading based on device
            torch_dtype = torch.float32 if device == "cpu" else torch.float16
            
            base_model = AutoModelForCausalLM.from_pretrained(
                BASE_MODEL_ID,
                device_map=device,
                torch_dtype=torch_dtype,
                trust_remote_code=True,
                low_cpu_mem_usage=True
            )
            
            self.model = PeftModel.from_pretrained(base_model, ADAPTER_PATH)
            print("Local LLM Loaded Successfully.")
        except Exception as e:
            print(f"Failed to load Local LLM: {e}")
            self.model = None

    def generate_response(self, prompt: str) -> str:
        if not self.model:
            return "Error: Local model is not loaded (check server logs/RAM)."
            
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=250,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        except Exception as e:
            return f"Error generating local response: {str(e)}"

# Singleton usage
# model_instance = LocalLLM.get_instance()
# response = model_instance.generate_response("Question")
