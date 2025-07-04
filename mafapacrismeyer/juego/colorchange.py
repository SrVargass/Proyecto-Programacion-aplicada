import pygame

# Get the pixels

def change_color(surface, from_hue, to_hue):
    pixels = pygame.PixelArray(surface)
    # Iterate over every pixel                             
    for x in range(surface.get_width()):
        for y in range(surface.get_height()):
            # Turn the pixel data into an RGB tuple
            rgb = surface.unmap_rgb(pixels[x][y])
            # Get a new color object using the RGB tuple and convert to HSLA
            color = pygame.Color(*rgb)
            h, s, l, a = color.hsla
            # Add 120 to the hue (or however much you want) and wrap to under 360
            color.hsla = (int(h) -from_hue + to_hue) % 360, int(s), int(l), int(a)
            # Assign directly to the pixel
            pixels[x][y] = color
    # The old way of closing a PixelArray object
    del pixels

