import torch
from PIL import Image
from flask import Flask, request, jsonify
from transformers import AutoProcessor, Blip2ForConditionalGeneration
from peft import LoraConfig, get_peft_model
import io

app = Flask(__name__)

BLIP2_SHRADED_MODEL_PATH = "./data/models/huggingface/models--ybelkada--blip2-opt-2.7b-fp16-sharded/snapshots/5c169c86c274058d9fa5359e8049ce3010d6c957/"

# Load models and processor
processor = AutoProcessor.from_pretrained("Salesforce/blip2-opt-2.7b")
model = Blip2ForConditionalGeneration.from_pretrained(BLIP2_SHRADED_MODEL_PATH, device_map="auto", load_in_8bit=True, local_files_only=True)

# Configure LoRA
config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    bias="none",
    target_modules=["q_proj", "k_proj"]
)
model = get_peft_model(model, config)

# Load LoRA weights
model_save_path = "/data/models/model.pt"
full_state_dict = torch.load(model_save_path)
lora_state_dict = {k: v for k, v in full_state_dict.items() if 'lora_' in k}
model.load_state_dict(lora_state_dict, strict=False)
del full_state_dict
torch.cuda.empty_cache()

device = "cuda" if torch.cuda.is_available() else "cpu"

@app.route('/generate_caption', methods=['POST'])
def generate_caption():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    file = request.files['image']
    image = Image.open(io.BytesIO(file.read())).convert('RGB')
    
    inputs = processor(images=image, return_tensors="pt").to(device, torch.float16)
    pixel_values = inputs.pixel_values
    
    generated_ids = model.generate(pixel_values=pixel_values, max_length=100)
    generated_caption = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    
    return jsonify({"caption": generated_caption})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
