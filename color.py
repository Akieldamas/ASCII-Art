import PIL
from PIL import Image
from PIL import ImageFilter
import shutil

ascii_keys = [" ", "-", "+"] # for a "minimalist" version
more_keys = [" ", ".", ":", "-", "=", "+", "*", "#", "%", "@"]

def image_to_ascii(image_path):
    #width = shutil.get_terminal_size().columns
    width = 50
    image = Image.open(image_path)

    aspect_ratio = image.height / image.width
    new_height = int(width * aspect_ratio * 0.55)
    image = image.resize((width, new_height))

    ascii_image = ""

    pixels = list(image.getdata())
    brightness_values = [(r + g + b) // 3 for r, g, b, a in pixels]
    min_pixel = min(brightness_values)
    max_pixel = max(brightness_values)

    for i in range(0, len(pixels), image.width):
        row = pixels[i:i+image.width]
        ascii_row = ""
        for pixel in row:
            r, g, b, a = pixel
            brightness = int((r + g + b) // 3)
            brightness = int((brightness - min_pixel) / (max_pixel - min_pixel) * 255)
            
            char_index = int(brightness / 255 * (len(more_keys) - 1))
            char = more_keys[char_index]
            ascii_row += f"\033[38;2;{r};{g};{b}m{char}\033[0m"
        
        ascii_image += ascii_row + "\n"
    
    print(ascii_image)

if __name__ == "__main__":
    image_to_ascii("assets/pixel_art.png")