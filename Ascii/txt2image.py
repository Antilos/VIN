import logging
from math import ceil
import glob, re
import time

from PIL import (
    Image,
    ImageFont,
    ImageDraw,
)

PIL_GRAYSCALE = 'L'
PIL_WIDTH_INDEX = 0
PIL_HEIGHT_INDEX = 1
COMMON_MONO_FONT_FILENAMES = [
    'DejaVuSansMono.ttf',  # Linux
    'Consolas Mono.ttf',   # MacOS, I think
    'Consola.ttf',         # Windows, I think
]

def textfile_to_image(textfile_path):
    """Convert text file to a grayscale image.

    arguments:
    textfile_path - the content of this file will be converted to an image
    font_path - path to a font file (for example impact.ttf)
    """
    # parse the file into lines stripped of whitespace on the right side
    with open(textfile_path) as f:
        lines = tuple(line.rstrip() for line in f.readlines())

    # choose a font (you can see more detail in the linked library on github)
    font = None
    # large_font = 20  # get better resolution with larger size
    # for font_filename in COMMON_MONO_FONT_FILENAMES:
    #     try:
    #         font = ImageFont.truetype(font_filename, size=large_font)
    #         print(f'Using font "{font_filename}".')
    #         break
    #     except IOError:
    #         print(f'Could not load font "{font_filename}".')
    if font is None:
        font = ImageFont.load_default()
        # print('Using default font.')

    # make a sufficiently sized background image based on the combination of font and lines
    font_points_to_pixels = lambda pt: round(pt * 96.0 / 72)
    margin_pixels = font_points_to_pixels(1)

    # height of the background image
    tallest_line = max(lines, key=lambda line: font.getsize(line)[PIL_HEIGHT_INDEX])
    max_line_height = font_points_to_pixels(font.getsize(tallest_line)[PIL_HEIGHT_INDEX])
    realistic_line_height = max_line_height * 0.8  # apparently it measures a lot of space above visible content
    image_height = int(ceil(realistic_line_height * len(lines) + 2 * margin_pixels))

    # width of the background image
    widest_line = max(lines, key=lambda s: font.getsize(s)[PIL_WIDTH_INDEX])
    max_line_width = font_points_to_pixels(font.getsize(widest_line)[PIL_WIDTH_INDEX])
    image_width = int(ceil(max_line_width + (2 * margin_pixels)))

    # draw the background
    background_color = 0  # black
    image = Image.new(PIL_GRAYSCALE, (image_width, image_height), color=background_color)
    draw = ImageDraw.Draw(image)

    # draw each line of text
    font_color = 255  # white
    # horizontal_position = margin_pixels
    horizontal_position = -100
    for i, line in enumerate(lines):
        vertical_position = int(round(margin_pixels + (i * realistic_line_height)))
        draw.text((horizontal_position, vertical_position), line, fill=font_color, font=font)

    return image

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    filenames = sorted(glob.glob("test_steps/*.txt"), key=lambda s : int(re.search(r'.*?_(\d+)\.txt', s).group(1)))

    image = textfile_to_image('test_out.txt')
    # image.show()
    image.save('generated.png')

    images = []
    t1 = time.time()
    for i, filename in enumerate(filenames):
        logging.info(f"Generating image from file {filename} ({i}/{len(filenames)})")
        img = textfile_to_image(filename)
        images.append(img)
    t2 = time.time()
    logging.info(f"Generating {len(filenames)} images took {t2-t1:.3f} seconds.")

    import imageio
    # images = []
    # for filename in filenames:
    #     images.append(imageio.imread(filename))
    fps = 60
    logging.info(f"Generating gif from {len(images)} images at {fps}fps:")
    t1 = time.time()
    imageio.mimsave('movie.gif', images, fps=fps)
    t2 = time.time()
    logging.info(f"Generating gif took {t2-t1:.3f} seconds.")