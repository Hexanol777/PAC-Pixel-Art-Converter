from image_funcs import quantize_colors, adjust_brightness, enhance_sharpness, adjust_vibrance
from PIL import Image

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