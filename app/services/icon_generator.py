import os
from PIL import Image, ImageOps, ImageEnhance
from PIL.ImageDraw import ImageDraw

def resize_image(image: Image.Image, size: tuple[int, int] = (64, 64)) -> Image.Image:
    """
    Resize the image to fit within the specified size while maintaining aspect ratio,
    adding padding if necessary.
    :param image: The image to be resized.
    :param size: A tuple containing the width and height to fit the image into.
    :return: A new image resized and padded to fit the specified size.
    """
    return ImageOps.fit(image, size, Image.Resampling.LANCZOS, centering=(0.5, 0.5))

def make_circular_mask(size: tuple[int, int]) -> Image.Image:
    """
    Create a circular mask of the specified size.
    :param size: A tuple containing the width and height of the mask.
    :return: A new image with a circular mask.
    """
    scale = 4
    big_size = (size[0] * scale, size[1] * scale)
    mask = Image.new("L", big_size, 0)
    draw = ImageDraw(mask)
    draw.ellipse((0, 0, big_size[0], big_size[1]), fill=255)
    mask = mask.resize(size, Image.Resampling.LANCZOS)
    return mask

def create_circular_background(background_color: tuple[int, int, int, int], size: tuple[int, int]) -> Image.Image:
    """
    Create a circular background image with the specified color and size.
    :param background_color: A tuple containing the RGBA values for the background color.
    :param size: A tuple containing the width and height of the background image.
    :return: A new image with a circular background.
    """
    mask = make_circular_mask(size)
    circle = Image.new("RGBA", size, background_color)
    background = Image.new("RGBA", size, (255, 255, 255, 0))
    background.paste(circle, (0, 0), mask)
    return background

def generate_3state_icon(image_path: str, app_name: str, circle_launcher_path: str) -> str:
    """
    Generate a 3-state icon from the given image.
    :param image_path: Path to the original PNG image.
    :param app_name: Name of the application to use for the icon.
    :param circle_launcher_path: Path to the Circle Launcher directory.
    :return: Path to the generated icon.
    """
    final_icon_size = (70, 70)

    # open the original image
    original_image = Image.open(image_path).convert("RGBA")

    # calculate background size
    icon_size = (original_image.width + 20, original_image.height + 20)

    states = []
    for state in ['normal', 'pressed', 'hover']:
        if state == 'normal':
            color = (0, 0, 0, 255)
            icon_state = original_image.copy()
        elif state == 'hover':
            color = (255, 255, 255, 255)
            icon_state = ImageEnhance.Color(original_image.copy()).enhance(1.2)
        else:
            color = (0, 0, 0, 200)
            icon_state = ImageEnhance.Brightness(original_image.copy()).enhance(0.8)

        background = create_circular_background(color, icon_size)
        composite = background.copy()
        offset = ((icon_size[0] - icon_state.width) // 2, (icon_size[1] - icon_state.height) // 2)
        composite.paste(icon_state, offset, icon_state)
        composite = resize_image(composite, final_icon_size)

        states.append(composite)

    final_image = Image.new("RGBA", (final_icon_size[0] * 3, final_icon_size[1]))

    for i, state in enumerate(states):
        final_image.alpha_composite(state, (i * final_icon_size[0], 0))

    app_path = os.path.join(circle_launcher_path, app_name)
    os.makedirs(app_path, exist_ok=True)
    output_path = os.path.join(app_path, f"{app_name}.png")

    if os.path.exists(output_path):
        os.remove(output_path)

    final_image.save(output_path, "PNG", optimize=True, quality=100, dpi=(300, 300))

    return str(output_path)
