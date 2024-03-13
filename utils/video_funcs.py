from image_funcs import quantize_colors, adjust_brightness, enhance_sharpness, adjust_vibrance
from PIL import Image
import imageio

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
    return frames

def create_video(images, output_file, fps=30):
    """
    Combine a list of PIL.Image objects into a video.

    Parameters:
        images (list): Has to be a list of PIL.Image objects.
        output_file (str): Path to the output video file, passed by another func.
        fps (int): Frames per second for the output video. Default is 30.
    """
    writer = imageio.get_writer(output_file, fps=fps)
    
    for img in images:
        img = img.convert("RGB")
        img_data = np.array(img)
        writer.append_data(img_data)
    
    writer.close()