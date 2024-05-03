<p align="center">
  <img src="https://github.com/Hexanol777/PAC-Pixel-Art-Converter/blob/main/lantern.ico" alt="PAC - Logo" />
</p>


# PAC - Pixel Art Converter

PAC (Pixel Art Converter) is a simple GUI application that allows you to convert images and videos into pixel art. It provides various options to manipulate images and videos, such as adjusting pixel size, color palette, brightness, sharpness, and vibrance.

<p align="center">
  <img src="https://github.com/Hexanol777/PAC-Pixel-Art-Converter/blob/main/READMEmd/PAC%20-%20Screenshot%202.png" alt="PAC - Screenshot 2" />
</p>

<p align="center">
  <img src="https://github.com/Hexanol777/PAC-Pixel-Art-Converter/blob/main/READMEmd/PAC%20-%20Screenshot%203.png" alt="PAC - Screenshot 3" />
</p>

## Features

- Import images and videos in almost all formats and view them in the application
- Resize the image to a chosen pixel size for a pixelated effect
- Adjust the color palette to control the number of colors in the image (16 - 25 recommended)
- Fine-tune sharpness to emphasize or soften the edges
- Manipulate brightness to lighten or darken the image
- Modify color vibrance to enhance or reduce color saturation
- Automatically determine the best parameter values for the images and videos
- Perpetual data augmentation for customized value determination
- Export the processed image or video in JPEG, PNG, or video format
- Display image operations in real-time
- Animated notifications for important messages

#### Auto Value determination

The Auto Value Determination feature employs a rather simple but effective algorithm to analyze the input image or video and suggest parameter values for pixel size, color palette, brightness, sharpness, and vibrance. Initially, it uses a set of 80 various points to evaluate the characteristics of the media and generate a preliminary set of parameter values. Over time, as the user continues to utilize the app and adjusts the settings according to their preferences, The algorithm dynamically adapts and refines its suggestions to better align with the user's taste. This iterative process ensures that the parameter values suggested by Auto Value Determination become increasingly more personalized to the user.

#### Key Bindings

```bash
Escape the App: `Esc` key
Reset results: `Backspace` key
Show/Hide changes: toggle `Shift_L`
```

## Requirements

- Python 3.6 or above
- Tkinter (typically included with Python)
- tkVideoPlayer
- Customtkinter
- OpenCV
- PIL (Python Imaging Library)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Hexanol777/PAC-Pixel-Art-Converter.git
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt

## Usage

1. Run the PAC application(this can also be done by running PAC - GUI.pyw):

   ```bash
   python pac-gui.py

2. Click on the "Import Image" button to select an image file from your computer.

3. Adjust the sliders for pixel size, color palette, brightness, sharpness, and vibrance to manipulate the image.

4. The image preview will update in real-time based on the chosen settings.

5. Once you are satisfied with the results, click on the "Export Image" button to save the processed image.

The exported images are structured in the below formatting scheme:

`NameGivenByUser` - `pixel_size` - `color_palette` - `brightness` - `sharpness` - `vibrance`

Image name serves as a record of the specific parameter values used during the image generation.
## Future Enhancements

- ~~Optimize image operations using NumPy for a faster execution time~~ minimal change noticed...
- ~~Change the structure of `init_parameters` for better data management.~~ Done!
- ~~Get the `Sharpness` parameter to work again~~ Done!
- ~~Add `Auto value determination`~~ Done!
- ~~Add `Video support`~~ Done!
- ~~Enhance overall theme and give it a modern look~~ Done!
- ~~`Dynamic GUI` changing based on the imported file~~ Done!
- ~~Add `Notifications`~~ Done!
- ~~Add `Key Binds`~~ Done!

## Examples
| ![LifeLine](https://github.com/Hexanol777/PAC-Pixel-Art-Converter/blob/main/input/2.jpg) | ![LifeLine](https://github.com/Hexanol777/PAC-Pixel-Art-Converter/blob/main/output/Lifeline%20-%205%20-%2075%20-%20100%20-%20100.png) |
| --- | --- |
| *LifeLine* | *LifeLine - Pixelized* |


| ![Lain](https://github.com/Hexanol777/PAC-Pixel-Art-Converter/blob/main/input/Lain.jpg) | ![Lain - Pixelized](https://github.com/Hexanol777/PAC-Pixel-Art-Converter/blob/main/output/Lain%20-%205%20-%2025%20-%20100%20-%20121.png) |
| --- | --- |
| *Lain* | *Lain - Pixelized* |



