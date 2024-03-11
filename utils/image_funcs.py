from PIL import Image, ImageEnhance

def resize_image_pixelsize(image, pixel_size):
    # Resize the image to the desired pixel size
    image = image.convert("RGB")
    new_width = image.size[1] // round(pixel_size)
    new_height = image.size[0] // round(pixel_size)
    resized_img_pixelsize = image.resize((new_width, 
                                               new_height),
                                                Image.LANCZOS)
    return resized_img_pixelsize

def quantize_colors(image, color_palette):
    # Reduce the color palette
    image = image.convert("RGB")
    quantized_image = image.quantize(colors=round(color_palette))
    return quantized_image

def adjust_brightness(image, brightness_factor):
    # Adjust the brightness of the image
    image = image.convert("RGB")
    brightness_float = brightness_factor / 100
    enhancer = ImageEnhance.Brightness(image)
    adjusted_image = enhancer.enhance(brightness_float)
    return adjusted_image

def enhance_sharpness(image, sharpness_factor): 
    # Enhance the sharpness of the image
    image = image.convert("RGB")
    sharpness_factor = sharpness_factor / 10
    enhancer = ImageEnhance.Sharpness(image)
    enhanced_image = enhancer.enhance(sharpness_factor)
    return enhanced_image

def adjust_vibrance(image, vibrance_factor):
    # Adjust the vibrance of the image
    image = image.convert("RGB")
    vibrance_float = vibrance_factor / 100
    enhancer = ImageEnhance.Color(image)
    vibrant_image = enhancer.enhance(vibrance_float)
    return vibrant_image