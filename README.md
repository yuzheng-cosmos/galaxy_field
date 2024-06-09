# Galaxy Field in Blender

Galaxy Field is a set of Python scripts designed to import galaxy images into Blender, automatically adjusting transparency, emission, and other properties to create stunning galaxy scenes.

![Screenshot](https://github.com/yuzheng-cosmos/galaxy_field/assets/7397493/63efd189-35e0-4f5c-aa5c-6e56ee6ee9e9)

## Features

- Import multiple galaxy images as planes in Blender.
- Automatically adjust emission and transparency properties.
- Randomly distribute images within a specified volume.
- Customizable transparency effects using color ramps.

## Getting Started

1. Eanable "Import Images as Planes" add-on
2. Run the script


### Script Parameters

- `image_folder`: The folder containing your galaxy images.
- `volume_size`: The size of the cube volume where images will be distributed.
- `num_images`: The number of images to import (use `None` to import all images).
- `color_ramp_positions`: Positions for the color ramp to adjust transparency (default is `[0.3, 0.7]`).


The file `save_crop.jsx` is an automated code for saving the Photoshop selection area to an image file. To use it, copy and paste the file to `/Applications/Adobe Photoshop 2024/Presets/Scripts`. In Photoshop, edit shortcuts and assign a shortcut key to `File > Scripts > save_crop`. Then, select a region in the image and press the hotkey to trigger the save selection script.
