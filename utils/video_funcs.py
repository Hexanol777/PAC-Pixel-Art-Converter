import cv2

def pixelize_video(video, pixel_size=10):

    video_capture = cv2.VideoCapture(input_video_path)

    # Get video properties
    frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(video_capture.get(cv2.CAP_PROP_FPS))

    # idk what this is tbh
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    # Read video
    while video_capture.isOpened():
        ret, frame = video_capture.read()

        if not ret:
            break

        # Pixelization effect
        small_frame = cv2.resize(frame, None, fx=1.0/pixel_size, fy=1.0/pixel_size, interpolation=cv2.INTER_NEAREST)
        pixelized_frame = cv2.resize(small_frame, (frame_width, frame_height), interpolation=cv2.INTER_NEAREST)

        # Write the pixelized frames
        video_writer.write(pixelized_frame)

    # Release the video
    video_capture.release()
    video_writer.release()
