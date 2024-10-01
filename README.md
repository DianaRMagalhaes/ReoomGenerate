
# Image Generator and Decorator

This project contains two main scripts: `image_generator.py` and `image_from_text.py`, which use image generation models and post-processing to create and enhance images based on provided text and image inputs.

## Prerequisites

Ensure you have the following packages installed before using this project:

- `torch`
- `PIL` (Pillow)
- `min_dalle`
- Any other packages specified in the imports (e.g., `ImageEnhance` from PIL).

You can install them with:
```bash
pip install torch Pillow min-dalle
```

## Files

### 1. `image_generator.py`

This file contains functions that generate images from text prompts using the `MinDalle` model. The key functionalities include:

- **`generate_image`**: Generates an image based on a text prompt using the `MinDalle` model.
- **`ascii_from_image`**: Converts a generated image to ASCII format.
- **`save_image`**: Saves the generated image to disk.
- **`generate_decorative_image`**: Generates a "decorative" image from a text prompt.
- **`decorate_image`**: Decorates an original image with another generated image.
- **`upscale_image`**: Upscales an image to a higher resolution.
- **`enhance_image`**: Enhances image quality by adjusting sharpness and contrast.

### 2. `image_from_text.py`

This file integrates image generation functionality with post-processing, allowing you to either decorate or enhance existing images, or simply generate new ones from text. The main functionalities include:

- **Load Image**: Loads an input image for decoration.
- **Generate Image**: Uses the text prompt to generate an image using the `MinDalle` model.
- **Decorate Image**: Decorates the original image with the generated image.
- **Upscale Image**: Increases the size of the final image.
- **Enhance Image**: Applies sharpness and contrast adjustments to the final image.
  
### Usage

#### Generate Simple Image
To generate an image based on a text prompt:

```bash
python image_generator.py --text "Image description" --seed 42 --grid_size 1 --top_k 256 --image_path "./output.png"
```

#### Decorate an Image
To decorate an input image with one generated from a text prompt:

```bash
python image_from_text.py --input_image "./my_image.png" --text "Decoration to apply" --seed 42 --upscale --sharpness 2.0 --contrast 1.5
```

#### Key Parameters

- **`--text`**: The text prompt used to generate the image.
- **`--seed`**: Sets the seed for consistent image generation.
- **`--grid_size`**: Controls the grid size of the generated image.
- **`--top_k`**: Specifies how many top results the model should use.
- **`--upscale`**: Upscales the final image.
- **`--sharpness`**: Adjusts the sharpness of the image.
- **`--contrast`**: Adjusts the contrast of the image.
