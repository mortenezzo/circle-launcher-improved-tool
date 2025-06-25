import os
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance

def generate_3state_icon(image_path: str, app_name: str, rainmeter_path: Path) -> str:
    """
    Generate a 3-state icon from the given image.
    :param image_path: Path to the original PNG image.
    :param app_name: Name of the application to use for the icon.
    :param rainmeter_path: Path to the Rainmeter skins directory.
    :return: Path to the generated icon.
    """
    app_path = rainmeter_path.joinpath(app_name)
    original = Image.open(image_path).convert("RGBA")
    w, h = original.size

    hovered = ImageOps.invert(original.convert("RGB")).convert("RGBA")
    down = ImageEnhance.Brightness(original).enhance(0.6).convert("RGBA")

    result = Image.new("RGBA", (w * 3, h))
    result.paste(original, (0, 0))
    result.paste(hovered, (w, 0))
    result.paste(down, (w * 2, 0))

    output_path = app_path.joinpath(f"{app_name}.png")

    result.save(output_path)

    return str(output_path)
