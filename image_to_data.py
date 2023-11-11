from PIL import Image
import numpy as np


def convert_image_to_list(image_file: str) -> object:
    """Converts image to list of RGB values"""
    with Image.open(image_file) as file:
        image_size = file.size
        if image_size[0] > image_size[1]:
            aspect_ratio = image_size[0] / 300
            new_size = (300, int(image_size[1] / aspect_ratio))
        else:
            aspect_ratio = image_size[1] / 300
            new_size = (int(image_size[0] / aspect_ratio), 300)
        image = file.convert("RGB").resize(new_size)
        print("File opened")
        # converting image to numpy array
        image_array = np.array(image)
        print("Image converted to array")
        image_array = image_array.flatten()
        print("Image flattened")
        return image_array.tolist()


# # convert_image_to_list("ImageFiles/Shubhendu.JPG")
# print(convert_image_to_list("ImageFiles/Shubhendu.JPG"))