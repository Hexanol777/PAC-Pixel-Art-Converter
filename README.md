<p align="center">
  <img src="https://github.com/Hexanol777/PAC-Pixel-Art-Converter/blob/main/lantern.ico" alt="PAC - Logo" />
</p>


# PAC - Pixel Art Converter

PAC (Pixel Art Converter) is a simple GUI application that allows you to convert images into pixel art. It provides various options to manipulate the image, such as adjusting pixel size, color palette, brightness, sharpness, and vibrance.

<p align="center">
  <img src="https://github.com/Hexanol777/PAC-Pixel-Art-Converter/blob/main/READMEmd/PAC%20-%20Screenshot%202.png" alt="PAC - screenshot" />
</p>

## Features

- Import images in almost all formats and view them in the application
- Resize the image to a chosen pixel size for a pixelated effect
- Adjust the color palette to control the number of colors in the image (16 - 25 recommended)
- Fine-tune sharpness to emphasize or soften the edges
- Manipulate brightness to lighten or darken the image
- Modify color vibrance to enhance or reduce color saturation
- Automatically determine the best parameter values for the images
- perpetual data augmentation for a customized value determination
- Export the processed image in JPEG or PNG
- Display image operations in real-time

## Requirements

- Python 3.6 or above
- Tkinter (typically included with Python)
- Customtkinter
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

`NameGivenByUser` - `pixel_size` - `color_palette` - `brightness` - `vibrance`

Image name serves as a record of the specific parameter values used during the image generation
## Future Enhancements

- Optimize image operations using NumPy for a faster execution time
- Change the structure of init_parameters for better data management.
- Get the `Sharpness` parameter to work again

## Examples
| ![LifeLine](https://github.com/Hexanol777/PAC-Pixel-Art-Converter/blob/main/input/2.jpg) | ![LifeLine](https://github.com/Hexanol777/PAC-Pixel-Art-Converter/blob/main/output/Lifeline%20-%205%20-%2075%20-%20100%20-%20100.png) |
| --- | --- |
| *LifeLine* | *LifeLine - Pixelized* |


| ![Lain](https://github.com/Hexanol777/PAC-Pixel-Art-Converter/blob/main/input/Lain.jpg) | ![Lain - Pixelized](https://github.com/Hexanol777/PAC-Pixel-Art-Converter/blob/main/output/Lain%20-%205%20-%2025%20-%20100%20-%20121.png) |
| --- | --- |
| *Lain* | *Lain - Pixelized* |



