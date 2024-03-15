from image_funcs import quantize_colors, adjust_brightness, enhance_sharpness, adjust_vibrance
from PIL import Image
import imageio
import numpy as np
import cv2

def resize_video_pixelsize(image, pixel_size):
    # Resize the image to the desired pixel size
    image = image.convert("RGB")
    width, height = image.size
    new_width = width // pixel_size
    new_height = height // pixel_size
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
        return frames
    
    # Reading till the video is complete
    while cap.isOpened():
        # Capture frames
        ret, frame = cap.read()
        if ret:
            # Convert colors
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convert the np array to pil
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
        output_file (str): Path to the output video file, passed by another func.
        fps (int): Frames per second for the output video. Default is 60.
    """
    writer = imageio.get_writer(output_file, fps=fps)
    
    for img in images:
        img = img.convert("RGB")
        img_data = np.array(img)
        writer.append_data(img_data)
    
    writer.close()

def process_video(video_path, output_video_path, pixel_size, color_palette, brightness_factor, sharpness_factor, vibrance_factor):

    frame_list, fps = extract_frames(video_path)
    transformed_frames = []

    for frame in frame_list:
        # Apply the pipeline to the frame
        frame = resize_video_pixelsize(frame, pixel_size)
        frame = quantize_colors(frame, color_palette)
        frame = adjust_brightness(frame, brightness_factor)
        frame = enhance_sharpness(frame, sharpness_factor)
        frame = adjust_vibrance(frame, vibrance_factor)
        # Append to list
        transformed_frames.append(frame)

    # Generate video
    create_video(transformed_frames, output_video_path, fps)