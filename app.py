import io
import modal
from PIL import Image
import os
import torch
from diffusers import StableDiffusionPipeline

app = modal.App("text-to-image")
image = modal.Image.debian_slim(python_version="3.10").pip_install(
    "numpy<2", 
    "torch==2.0.1",
    "torchvision==0.15.2",
    "diffusers==0.19.3",
    "transformers==4.32.1",
    "accelerate==0.21.0",
    "safetensors==0.3.3",
    "Pillow==10.0.0",
    "xformers==0.0.20",
    "huggingface_hub==0.15.1",
)

# Create a volume
volume = modal.Volume.from_name("model-cache", create_if_missing=True)

@app.function(
    image=image,
    gpu=modal.gpu.A10G(),
    volumes={"/cache": volume},
    timeout=300,
)
def generate_image(prompt: str, negative_prompt: str = "", num_inference_steps: int = 20, guidance_scale: float = 7.5):
    """
    Generate an image from text prompt using Stable Diffusion
    """
    os.environ["TRANSFORMERS_CACHE"] = "/cache"
    os.environ["HF_HOME"] = "/cache"
    try:
        # Load the model
        pipe = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float16,
            cache_dir="/cache",
        )
        pipe = pipe.to("cuda")
        pipe.enable_attention_slicing()
        
        # Generate image
        with torch.autocast("cuda"):
            image = pipe(
                prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
            ).images[0]
        
        # Convert to bytes
        img_buffer = io.BytesIO()
        image.save(img_buffer, format="PNG")
        img_buffer.seek(0)
        
        return img_buffer.getvalue()
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

@app.function(
    image=image,
    gpu=modal.gpu.A10G(),
    volumes={"/cache": volume},
    timeout=600,
)
def generate_multiple_images(prompts: list, negative_prompt: str = "", num_inference_steps: int = 20, guidance_scale: float = 7.5):
    """
    Generate multiple images from a list of prompts
    """
    os.environ["TRANSFORMERS_CACHE"] = "/cache"
    os.environ["HF_HOME"] = "/cache"
    try:
        # Load the model
        pipe = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float16,
            cache_dir="/cache",
        )
        pipe = pipe.to("cuda")
        pipe.enable_attention_slicing()
        
        results = []
        
        for prompt in prompts:
            with torch.autocast("cuda"):
                image = pipe(
                    prompt,
                    negative_prompt=negative_prompt,
                    num_inference_steps=num_inference_steps,
                    guidance_scale=guidance_scale,
                ).images[0]
            
            img_buffer = io.BytesIO()
            image.save(img_buffer, format="PNG")
            img_buffer.seek(0)
            
            results.append({
                "prompt": prompt,
                "image_data": img_buffer.getvalue()
            })
        
        return results
    except Exception as e:
        print(f"Error generating multiple images: {e}")
        return []

@app.local_entrypoint()
def main():
    # Test with a simple prompt
    prompt = "A beautiful sunset over mountains, digital art"
    print(f"Generating image for prompt: {prompt}")
    
    image_data = generate_image.remote(prompt)
    with open("generated_image.png", "wb") as f:
        f.write(image_data)
    
    print("Image saved as 'generated_image.png'")

if __name__ == "__main__":
    main()