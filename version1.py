import PIL.Image as PIL
import shutil

ascii_keys = [" ", "-", "+"]
more_keys = [" ", ".", ":", "-", "=", "+", "*", "#", "%", "@"]

def image_to_ascii(image_path):
    #width = shutil.get_terminal_size().columns
    width = 50
    gamma = 1.8 # < 1 for brighter, > 1 for darker
    image = PIL.open(image_path)

    aspect_ratio = image.height / image.width
    new_height = int(width * aspect_ratio * 0.55)
    image = image.resize((width, new_height))
    image = image.convert("L")

    ascii_image = ""

    pixels = list(image.getdata())

    for i in range(0, len(pixels), image.width):
        row = pixels[i:i+image.width]
        ascii_row = ""
        for pixel in row:
            pixel = int((pixel / 255) ** gamma * 255)
            char_index = int(pixel / 255 * (len(more_keys) - 1))
            char = more_keys[char_index]
            ascii_row += char
        
        ascii_image += ascii_row + "\n"
    
    print(ascii_image)

if __name__ == "__main__":
    image_to_ascii("assets/butterfly.png")