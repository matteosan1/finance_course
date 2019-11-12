from PIL import Image

def transform_images():
    out = []
    image_names = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "zero", "g"]
    for n in image_names:
        original = Image.open('{}.png'.format(n))
        width, height = original.size
        pixels = []
        for y in range(height):
            l = []
            for x in range(width):
                pixel = original.getpixel((x, y))
                g = 255 - ((pixel[0] * 0.299) + (pixel[1] * 0.587) + (pixel[2] * 0.114))
                l.append(g)
            pixels.append(l)
        out.append(pixels)

    return out

def transform_image(file_name):
    out = []
    original = Image.open(file_name)
    im = original.resize((28, 28), Image.ANTIALIAS)
    width, height = im.size
    pixels = []
    for y in range(height):
        l = []
        for x in range(width):
            pixel = im.getpixel((x, y))
            g = 255 - ((pixel[0] * 0.299) + (pixel[1] * 0.587) + (pixel[2] * 0.114))
            l.append(g)
        pixels.append(l)
    out.append(pixels)

    return out

if __name__ == "__main__":
    transform_image("five.png")
