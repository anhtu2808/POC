from llama_cpp import Llama
from app.core.config import settings
import json
import re

class LLMService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLMService, cls).__new__(cls)
            print(f"Loading LLM from {settings.MODEL_PATH}...")
            cls._instance.llm = Llama(
                model_path=settings.MODEL_PATH,
                n_ctx=4096,  # Context window
                n_gpu_layers=-1, # Offload all to GPU (Metal)
                verbose=False
            )
            print("LLM Loaded successfully.")
        return cls._instance

    def extract_resume_data(self, text: str) -> dict:
        # Llama 3 specific prompt format without manual BOS token
        prompt = f"""<|start_header_id|>system<|end_header_id|>
You are an expert Resume Parser. Your task is to extract structured information from the resume text provided by the user.
You must output ONLY valid JSON. Do not include any explanation, preamble, or markdown formatting (like ```json).

Required Fields:
- summary (string): A brief professional summary or objective.
- experience (list of strings): List of work experience entries (Company, Role, Dates, Description).
- education (list of strings): List of educational qualifications.
- skills (list of strings): List of technical and soft skills.

If a section is missing, use an empty list/string. Ensure strings are properly escaped.
<|eot_id|><|start_header_id|>user<|end_header_id|>

Resume Text:
{text[:3500]} 
<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""

        response = self.llm(
            prompt,
            max_tokens=settings.MAX_TOKENS,
            stop=["<|eot_id|>"],
            echo=False,
            temperature=0.1,
            top_p=0.9
        )
        
        output_text = response["choices"][0]["text"].strip()
        
        # Robust JSON extraction using json_repair
        try:
            import json_repair
            return json_repair.loads(output_text)
        except ImportError:
            # Fallback if library not installed (though we added it)
            print("json_repair module not found. Falling back to standard json.")
            try:
                # Basic cleanup
                output_text = output_text.replace("'", '"') # Sometimes LLMs use single quotes
                return json.loads(output_text)
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON. Raw output: {output_text[:100]}... Error: {e}")
                return {
                    "summary": "Parsing failed",
                    "experience": [],
                    "education": [],
                    "skills": []
                }
        except Exception as e:
            print(f"json_repair failed: {e}")
            return {
                "summary": "Parsing failed",
                "experience": [],
                "education": [],
                "skills": []
            }

llm_service = LLMService()
