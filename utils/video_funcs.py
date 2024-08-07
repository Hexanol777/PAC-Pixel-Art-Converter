from image_funcs import quantize_colors, adjust_brightness, enhance_sharpness, adjust_vibrance
from PIL import Image
import imageio
import numpy as np
import cv2
import os
from concurrent.futures import ThreadPoolExecutor

def resize_video_pixelsize(image, pixel_size):
    # Resize the image to the desired pixel size
    image = image.convert("RGB")
    width, height = image.size
    new_width = width // round(pixel_size)
    new_height = height // round(pixel_size)
    resized_img_pixelsize = image.resize((new_width, new_height), Image.NEAREST)
    final_resized_img = resized_img_pixelsize.resize((width, height), Image.NEAREST)
    return final_resized_img

def extract_frames(video_path):
    frames = []
    # Open the video
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if not cap.isOpened():
        print("Error: Unable to open video file")
        return frames, fps
    
    # Reading till the video is complete
    while cap.isOpened():
        # Capture frames
        ret, frame = cap.read()
        if ret:
            # Convert colors
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convert the np array to PIL Image
            image = Image.fromarray(frame_rgb)
            # Append the image
            frames.append(image)
        else:
            break
    
    # Release the video
    cap.release()
    return frames, fps

def create_video(images, output_file, fps=60):
    """
    Combine a list of PIL.Image objects into a video.

    Parameters:
        images (list): Has to be a list of PIL.Image objects.
        fps (int): Frames per second for the output video. Default is 60.
    """
    if not os.path.exists("./temp"):
        os.mkdir("./temp")
    writer = imageio.get_writer(output_file, fps=fps)
    for img in images:
        img = img.convert("RGB")
        img_data = np.array(img)
        writer.append_data(img_data)
    writer.close()
    print(output_file)

def process_frame(frame, pixel_size, color_palette, brightness_factor, sharpness_factor, vibrance_factor):
    # Apply the pipeline to the frame
    frame = resize_video_pixelsize(frame, pixel_size)
    frame = quantize_colors(frame, color_palette)
    frame = adjust_brightness(frame, brightness_factor)
    frame = enhance_sharpness(frame, sharpness_factor)
    frame = adjust_vibrance(frame, vibrance_factor)
    return frame

def process_video(video_path, pixel_size, color_palette, brightness_factor, sharpness_factor, vibrance_factor):
    print(pixel_size, color_palette, brightness_factor, sharpness_factor, vibrance_factor)
    frame_list, fps = extract_frames(video_path)

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor() as executor:
        # Map each frame to the processing function
        transformed_frames = list(executor.map(
            process_frame,
            frame_list,
            [pixel_size] * len(frame_list),
            [color_palette] * len(frame_list),
            [brightness_factor] * len(frame_list),
            [sharpness_factor] * len(frame_list),
            [vibrance_factor] * len(frame_list)
        ))

    parameter_values = f'{round(pixel_size)}' \
                       f' - {round(color_palette)}' \
                       f' - {round(brightness_factor)}' \
                       f' - {round(sharpness_factor)}' \
                       f' - {round(vibrance_factor)}'

    output_file = os.path.splitext(video_path)[0] + f" - {parameter_values}.mp4"
    filename = "temp/" + os.path.basename(output_file)

    # Generate video
    create_video(transformed_frames, filename, fps)
    
    return filename
