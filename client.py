import modal
import argparse
from datetime import datetime
import os

def save_image(image_data: bytes, filename: str = None):
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_image_{timestamp}.png"
    
    with open(filename, "wb") as f:
        f.write(image_data)
    return filename

def main():
    parser = argparse.ArgumentParser(description="Generate images using Modal text-to-image service")
    parser.add_argument("prompt", help="Text prompt for image generation")
    parser.add_argument("--negative-prompt", default="", help="Negative prompt (what to avoid)")
    parser.add_argument("--steps", type=int, default=20, help="Number of inference steps")
    parser.add_argument("--guidance", type=float, default=7.5, help="Guidance scale")
    parser.add_argument("--output", help="Output filename (default: auto-generated)")
    parser.add_argument("--multiple", nargs="+", help="Generate multiple images from multiple prompts")
    
    args = parser.parse_args()
    app = modal.App.lookup("text-to-image", create_if_missing=False)

    if args.multiple:
        print(f"Generating {len(args.multiple)} images...")
        generate_multiple_images = modal.Function.from_name("text-to-image", "generate_multiple_images")
        results = generate_multiple_images.remote(
            prompts=list(args.multiple),
            negative_prompt=args.negative_prompt,
            num_inference_steps=args.steps,
            guidance_scale=args.guidance
        )
        if not results:
            print("Failed to generate images. Please check Modal logs for errors.")
            return
        for i, result in enumerate(results):
            if not result or not result.get("image_data"):
                print(f"Failed to generate image for prompt: {result.get('prompt', 'unknown')}")
                continue
            filename = f"image_{i+1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            save_image(result["image_data"], filename)
            print(f"Generated image {i+1}: {filename}")
            print(f"  Prompt: {result['prompt']}")
    else:
        print(f"Generating image for prompt: {args.prompt}")
        generate_image = modal.Function.from_name("text-to-image", "generate_image")
        image_data = generate_image.remote(
            prompt=args.prompt,
            negative_prompt=args.negative_prompt,
            num_inference_steps=args.steps,
            guidance_scale=args.guidance
        )
        if not image_data:
            print("Failed to generate image. Please check Modal logs for errors.")
            return
        filename = save_image(image_data, args.output)
        print(f"Image saved as: {filename}")

if __name__ == "__main__":
    main()