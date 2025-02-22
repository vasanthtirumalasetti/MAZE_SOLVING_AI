import os
from matplotlib.image import imsave
import numpy as np
import PIL
import cv2
from time import time
from collections import deque

# Set default folder path
DEFAULT_FOLDER_PATH = "D:\\hackathon\\Maze\\input"

def preprocess_image(img_path):
    img = np.asarray(PIL.Image.open(img_path).convert('L'))
    binary_img = (img > 128).astype(np.uint8) * 255
    return binary_img

def find_start_end(binary_img):
    start, end = None, None

    for j in range(binary_img.shape[1]):
        if binary_img[0, j] == 255:
            start = (0, j)
        if binary_img[-1, j] == 255:
            end = (binary_img.shape[0] - 1, j)

    if start and end:
        return start, end

    for i in range(binary_img.shape[0]):
        if binary_img[i, 0] == 255:
            start = (i, 0)
        if binary_img[i, -1] == 255:
            end = (i, binary_img.shape[1] - 1)

    if start and end:
        return start, end

    raise ValueError("Start or end point not found in the maze.")

def optimized_flooding_search(binary_img, start, end):
    rows, cols = binary_img.shape
    neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    queue = deque([start])
    came_from = {}
    visited = np.zeros(binary_img.shape, dtype=bool)
    visited[start] = True

    while queue:
        current = queue.popleft()
        if current == end:
            break

        for dx, dy in neighbors:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if binary_img[neighbor] == 255 and not visited[neighbor]:
                    queue.append(neighbor)
                    visited[neighbor] = True
                    came_from[neighbor] = current
                    if neighbor == end:
                        return came_from

    return came_from

def reconstruct_path(came_from, start, end):
    path = []
    current = end
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

def optimized_visualize_maze(binary_img, path, explored, path_thickness=3):
    color_img = np.zeros((*binary_img.shape, 3), dtype=np.uint8)
    color_img[binary_img == 255] = [255, 255, 255]
    color_img[binary_img == 0] = [0, 0, 0]

    # Mark explored cells in red
    explored = np.array(explored)
    color_img[explored[:, 0], explored[:, 1]] = [255, 0, 0]

    # Create a separate mask for the path and draw the path in green with increased thickness
    path_img = np.zeros(binary_img.shape, dtype=np.uint8)
    for r, c in path:
        path_img[r, c] = 255

    # Use OpenCV to dilate the path to increase thickness
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (path_thickness, path_thickness))
    thick_path = cv2.dilate(path_img, kernel)

    color_img[thick_path > 0] = [0, 255, 0]  # Draw the thick green path

    return color_img

def main():
    folder_path = DEFAULT_FOLDER_PATH

    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return

    # Get all image files in the folder
    supported_formats = [".png", ".jpg", ".jpeg", ".bmp", ".gif"]
    image_files = [f for f in os.listdir(folder_path) if os.path.splitext(f)[1].lower() in supported_formats]

    if not image_files:
        print("No supported image files found in the folder.")
        return

    output_folder = os.path.join(folder_path, "solved_mazes")
    os.makedirs(output_folder, exist_ok=True)

    for image_file in image_files:
        img_path = os.path.join(folder_path, image_file)
        print(f"Processing: {image_file}")

        binary_img = preprocess_image(img_path)
        try:
            start, end = find_start_end(binary_img)
        except ValueError as e:
            print(f"Error: {e} in {image_file}")
            continue

        print("Solving the maze...")
        st_time = time()
        came_from = optimized_flooding_search(binary_img, tuple(start), tuple(end))
        if not came_from:
            print(f"No solution found for {image_file}.")
            continue

        path = reconstruct_path(came_from, tuple(start), tuple(end))
        explored = list(came_from.keys())
        print(f"Maze {image_files.index(image_file) + 1}/{len(image_files)} solved in {time() - st_time:.2f} seconds.")

        print("Visualizing the solution...")
        result_img = optimized_visualize_maze(binary_img, path, explored)
        
        output_path = os.path.join(output_folder, f"solved_{image_file}")
        PIL.Image.fromarray(result_img).save(output_path)
        print(f"Solution saved as {output_path}")

if __name__ == "__main__":
    main()
