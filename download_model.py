from huggingface_hub import hf_hub_download
import os

# Model details
MODEL_REPO = "bartowski/Llama-3.2-1B-Instruct-GGUF"
MODEL_FILE = "Llama-3.2-1B-Instruct-Q4_K_M.gguf"
LOCAL_DIR = "./llm/models"

print(f"Downloading {MODEL_FILE} from {MODEL_REPO}...")
print(f"Target directory: {os.path.abspath(LOCAL_DIR)}")

try:
    path = hf_hub_download(
        repo_id=MODEL_REPO,
        filename=MODEL_FILE,
        local_dir=LOCAL_DIR,
        local_dir_use_symlinks=False
    )
    print(f"✅ Model downloaded successfully to: {path}")
    print("You can now run the application.")
except Exception as e:
    print(f"❌ Error downloading model: {e}")
