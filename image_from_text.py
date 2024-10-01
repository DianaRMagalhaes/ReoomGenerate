import argparse
import os
from PIL import Image, ImageEnhance
from min_dalle import MinDalle
import torch

# Definição dos argumentos de linha de comando
parser = argparse.ArgumentParser()
parser.add_argument('--mega', action='store_true')
parser.add_argument('--no-mega', dest='mega', action='store_false')
parser.set_defaults(mega=False)
parser.add_argument('--fp16', action='store_true')
parser.add_argument('--text', type=str, default='Dali painting of WALL·E')
parser.add_argument('--seed', type=int, default=-1)
parser.add_argument('--grid-size', type=int, default=1)
parser.add_argument('--image-path', type=str, default='generated')
parser.add_argument('--models-root', type=str, default='our_model')
parser.add_argument('--top_k', type=int, default=256)
parser.add_argument('--input-image', type=str, help="Path to the input image to be transformed")
parser.add_argument('--upscale', action='store_true', help="If set, upscale the final image")
parser.add_argument('--sharpness', type=float, default=1.0, help="Enhance sharpness of the image")
parser.add_argument('--contrast', type=float, default=1.0, help="Enhance contrast of the image")

# Função para converter uma imagem em ASCII art
def ascii_from_image(image: Image.Image, size: int = 128) -> str:
    gray_pixels = image.resize((size, int(0.55 * size))).convert('L').getdata()
    chars = list('.,;/IOX')
    chars = [chars[i * len(chars) // 256] for i in gray_pixels]
    chars = [chars[i * size: (i + 1) * size] for i in range(size // 2)]
    return '\n'.join(''.join(row) for row in chars)

# Função para salvar uma imagem no caminho especificado
def save_image(image: Image.Image, path: str):
    if os.path.isdir(path):
        path = os.path.join(path, 'generated.png')
    elif not path.endswith('.png'):
        path += '.png'
    print("Saving image to", path)
    image.save(path)
    return image

# Função para carregar uma imagem a partir de um caminho
def load_image(image_path: str) -> Image.Image:
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"The image path '{image_path}' does not exist.")
    print(f"Loading image from {image_path}")
    return Image.open(image_path)

# Função para gerar uma imagem usando o modelo MinDalle
def generate_image(
    is_mega: bool,
    text: str,
    seed: int,
    grid_size: int,
    top_k: int,
    image_path: str,
    models_root: str,
    fp16: bool,
) -> Image.Image:
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

# Função para gerar uma imagem decorativa baseada em um prompt
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

# Função para decorar uma imagem original com uma imagem decorativa
def decorate_image(original_image: Image.Image, decoration_image: Image.Image) -> Image.Image:
    original_image = original_image.convert("RGBA")
    decoration_image = decoration_image.resize(original_image.size).convert("RGBA")

    # Ajusta a transparência da imagem decorativa para permitir que a imagem original seja visível
    alpha = decoration_image.split()[3]  # Obtém o canal alfa (transparência)
    alpha = alpha.point(lambda p: p * 0.5)  # Ajusta a transparência para 50%
    decoration_image.putalpha(alpha)

    decorated_image = Image.alpha_composite(original_image, decoration_image)
    return decorated_image.convert("RGB")

# Função para redimensionar a imagem final para uma resolução maior
def upscale_image(image: Image.Image, scale_factor: int = 2) -> Image.Image:
    new_size = (image.width * scale_factor, image.height * scale_factor)
    return image.resize(new_size, Image.LANCZOS)

# Função para aplicar pós-processamento para melhorar a qualidade da imagem
def enhance_image(image: Image.Image, sharpness: float, contrast: float) -> Image.Image:
    if sharpness != 1.0:
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(sharpness)
    if contrast != 1.0:
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(contrast)
    return image

# Função principal que integra todas as funcionalidades
def main():
    args = parser.parse_args()
    print(args)
    
    if args.input_image:
        # Carregar imagem de entrada
        original_image = load_image(args.input_image)
        
        # Gerar uma imagem decorativa com base no prompt de texto
        decoration_image = generate_decorative_image(
            prompt=args.text,
            is_mega=args.mega,
            seed=args.seed,
            models_root=args.models_root,
            fp16=args.fp16
        )
        
        # Decorar a imagem original com a imagem gerada
        final_image = decorate_image(original_image, decoration_image)
    else:
        # Gerar a imagem diretamente
        final_image = generate_image(
            is_mega=args.mega,
            text=args.text,
            seed=args.seed,
            grid_size=args.grid_size,
            top_k=args.top_k,
            image_path=args.image_path,
            models_root=args.models_root,
            fp16=args.fp16,
        )

    # Verificar se a imagem deve ser ampliada
    if args.upscale:
        final_image = upscale_image(final_image)

    # Aplicar melhorias de qualidade
    final_image = enhance_image(final_image, args.sharpness, args.contrast)

    # Salvar a imagem final decorada ou gerada
    save_image(final_image, args.image_path)
    print(ascii_from_image(final_image, size=128))

if __name__ == '__main__':
    main()
