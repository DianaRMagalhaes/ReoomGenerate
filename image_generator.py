import os
from PIL import Image
from min_dalle import MinDalle
import torch

def ascii_from_image(image: Image.Image, size: int = 128) -> str:
    gray_pixels = image.resize((size, int(0.55 * size))).convert('L').getdata()
    chars = list('.,;/IOX')
    chars = [chars[i * len(chars) // 256] for i in gray_pixels]
    chars = [chars[i * size: (i + 1) * size] for i in range(size // 2)]
    return '\n'.join(''.join(row) for row in chars)

def save_image(image: Image.Image, path: str):
    if os.path.isdir(path):
        path = os.path.join(path, 'generated.png')
    elif not path.endswith('.png'):
        path += '.png'
    print("saving image to", path)
    image.save(path)
    return image

def generate_image(
    is_mega: bool,
    text: str,
    seed: int,
    grid_size: int,
    top_k: int,
    image_path: str,
    models_root: str,
    fp16: bool,
):
    model = MinDalle(
        is_mega=is_mega, 
        models_root=models_root,
        is_reusable=False,
        is_verbose=True,
        dtype=torch.float16 if fp16 else torch.float32
    )

    image = model.generate_image(
        text, 
        seed, 
        grid_size, 
        top_k=top_k, 
        is_verbose=True
    )
    save_image(image, image_path)
    print(ascii_from_image(image, size=128))
    return image

def generate_decorative_image(prompt: str, is_mega: bool, seed: int, models_root: str, fp16: bool) -> Image.Image:
    return generate_image(
        is_mega=is_mega,
        text=prompt,
        seed=seed,
        grid_size=1,
        top_k=256,
        image_path="generated_decorative.png",
        models_root=models_root,
        fp16=fp16
    )

def decorate_image(original_image: Image.Image, decoration_image: Image.Image) -> Image.Image:
    original_image = original_image.convert("RGBA")
    decoration_image = decoration_image.resize(original_image.size).convert("RGBA")

    decorated_image = Image.alpha_composite(original_image, decoration_image)
    return decorated_image.convert("RGB")
