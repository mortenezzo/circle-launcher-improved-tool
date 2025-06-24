from PIL import Image, ImageOps, ImageEnhance
import os

def generate_3state_icon(image_path: str, output_path: str = None) -> str:
    """
    Generate a 3-state icon from the given image.
    :param image_path: Path to the input image.
    :param output_path: Path to save the generated icon. If None, it will save in the same directory as the input image with a .png extension.
    :return: Path to the generated icon.
    """
    original = Image.open(image_path).convert("RGBA")
    w, h = original.size

    hovered = ImageOps.invert(original.convert("RGB")).convert("RGBA")
    down = ImageEnhance.Brightness(original).enhance(0.6).convert("RGBA")

    result = Image.new("RGBA", (w * 3, h))
    result.paste(original, (0, 0))
    result.paste(hovered, (w, 0))
    result.paste(down, (w * 2, 0))

    if output_path is None:
        base = os.path.splitext(image_path)[0]
        output_path = base + ".png"

    result.save(output_path)
    return output_path
