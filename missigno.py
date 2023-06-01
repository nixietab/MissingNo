import cv2
import numpy as np
import os
import random

def randomize_silhouette(image_path, output_path):

    os.makedirs(output_directory_path, exist_ok=True)
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error loading image: {image_path}")
        return

    mask = np.zeros(image.shape[:2], np.uint8)

    background_model = np.zeros((1, 65), np.float64)
    foreground_model = np.zeros((1, 65), np.float64)

    rectangle = (1, 1, image.shape[1] - 1, image.shape[0] - 1)

    cv2.grabCut(image, mask, rectangle, background_model, foreground_model, 5, cv2.GC_INIT_WITH_RECT)

    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

    random_pixels = np.random.randint(0, 256, size=(image.shape[0], image.shape[1], 3), dtype=np.uint8)
    random_image = image * (1 - mask2[:, :, np.newaxis]) + random_pixels * mask2[:, :, np.newaxis]

    random_image = add_random_shapes(random_image, mask2)

    cv2.imwrite(output_path, random_image)

    print("Randomized image successfully!")


def add_random_shapes(image, mask):
    result = image.copy()

    for _ in range(10):
        shape = random.choice(["rectangle", "circle", "line"])
        x1 = random.randint(0, image.shape[1] - 1)
        y1 = random.randint(0, image.shape[0] - 1)
        x2 = random.randint(0, image.shape[1] - 1)
        y2 = random.randint(0, image.shape[0] - 1)

        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1

        if shape == "rectangle":
            cv2.rectangle(result, (x1, y1), (x2, y2), random_color(), -1)

        elif shape == "circle":
            width = x2 - x1
            height = y2 - y1
            if width > 1 and height > 1: 
                radius = min(random.randint(1, width // 2), random.randint(1, height // 2))
                center = (random.randint(x1 + radius, x2 - radius), random.randint(y1 + radius, y2 - radius))
                cv2.circle(result, center, radius, random_color(), -1)

        elif shape == "line":
            cv2.line(result, (x1, y1), (x2, y2), random_color(), 1)

    result = result * mask[:, :, np.newaxis]

    return result


def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


directory_path = "./"

output_directory_path = "./rando"

for filename in os.listdir(directory_path):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image_path = os.path.join(directory_path, filename)
        output_path = os.path.join(output_directory_path, filename)
        randomize_silhouette(image_path, output_path)
        print(f"Processed image: {filename}")

print("All images processed successfully!")
