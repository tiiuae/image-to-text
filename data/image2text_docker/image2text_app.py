import os
import time
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from transformers import AutoProcessor, AutoModelForCausalLM
from PIL import Image
import torch
import numpy as np
import io

app = FastAPI()

def setup_model():
    model_id = 'microsoft/Florence-2-large'
    torch.set_default_dtype(torch.float16)
    model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True, torch_dtype=torch.float16, device_map='cuda').eval().cuda()
    processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)
    return model, processor

model, processor = setup_model()

def run_inference(image, task_prompt):
    inputs = processor(text=task_prompt, images=image, return_tensors="pt").to('cuda', torch.float16)
    generated_ids = model.generate(
        input_ids=inputs["input_ids"].cuda(),
        pixel_values=inputs["pixel_values"].cuda(),
        max_new_tokens=128,
        early_stopping=False,
        do_sample=False,
        num_beams=3,
    )
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
    
    raw_caption = processor.post_process_generation(
        generated_text, 
        task=task_prompt, 
        image_size=(image.width, image.height)
    )
    
    # Extract the caption from the raw output
    if isinstance(raw_caption, dict):
        raw_caption = raw_caption.get('<MORE_DETAILED_CAPTION>', '')
    
    # Post-processing
    if not raw_caption:
        return "No caption could be generated for this image."
    
    if not raw_caption.endswith('.'):
        last_period = raw_caption.rfind('.')
        last_comma = raw_caption.rfind(',')
        
        if last_period != -1 and last_comma != -1:
            cut_index = max(last_period, last_comma)
        elif last_period != -1:
            cut_index = last_period
        elif last_comma != -1:
            cut_index = last_comma
        else:
            cut_index = len(raw_caption) - 1
        
        caption = raw_caption[:cut_index+1]
        
        if caption.endswith(','):
            caption = caption[:-1] + '.'
    else:
        caption = raw_caption
    
    # Ensure the caption ends with a period
    if not caption.endswith('.'):
        caption += '.'
    
    # Clean up any extra spaces
    caption = ' '.join(caption.split())
    
    return caption

def preprocess_image(image):
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    img_array = np.array(image)
    if len(img_array.shape) != 3 or img_array.shape[2] != 3:
        img_array = np.stack((img_array,)*3, axis=-1)
    
    return Image.fromarray(img_array)

def warm_up():
    test_image_path = 'test.jpg'
    if not os.path.exists(test_image_path):
        raise FileNotFoundError(f"Warm-up image '{test_image_path}' not found in the current directory.")
    
    warm_up_image = Image.open(test_image_path)
    warm_up_image = preprocess_image(warm_up_image)
    task_prompt = '<MORE_DETAILED_CAPTION>'
    
    for i in range(2):
        print(f"Performing warm-up {i+1}/2...")
        _ = run_inference(warm_up_image, task_prompt)
        print(f"Warm-up {i+1} completed.")

# Perform warm-up when the server starts
warm_up()

@app.post("/generate_image_caption")
async def generate_image_caption(image: UploadFile = File(...)):
    start_time = time.time()
    
    contents = await image.read()
    pil_image = Image.open(io.BytesIO(contents))
    pil_image = preprocess_image(pil_image)
    
    task_prompt = '<MORE_DETAILED_CAPTION>'
    result = run_inference(pil_image, task_prompt)
    
    end_time = time.time()
    inference_time = end_time - start_time
    
    return JSONResponse(content={
        "caption": result,
        "inference_time": f"{inference_time:.2f} seconds"
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
