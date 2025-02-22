import os
from matplotlib.image import imsave
import numpy as np
import PIL
import cv2
from time import time
from collections import deque
from tkinter import Tk, filedialog

def select_image():
    """Prompts user to select a single maze image."""
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select Maze Image",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )
    if not file_path:
        print("No file selected. Exiting.")
        exit()
    return file_path

def preprocess_image(img_path):
    """Converts an image to a binary maze format (black & white)."""
    img = np.asarray(PIL.Image.open(img_path).convert('L'))
    binary_img = (img > 128).astype(np.uint8) * 255  # Convert to binary (black/white)
    return binary_img

def find_start_end(binary_img):
    """Finds the start and end points of the maze from white (255) border pixels."""
    start, end = None, None

    for j in range(binary_img.shape[1]):  # Check first and last row
        if binary_img[0, j] == 255:
            start = (0, j)
        if binary_img[-1, j] == 255:
            end = (binary_img.shape[0] - 1, j)

    if start and end:
        return start, end

    for i in range(binary_img.shape[0]):  # Check first and last column
        if binary_img[i, 0] == 255:
            start = (i, 0)
        if binary_img[i, -1] == 255:
            end = (i, binary_img.shape[1] - 1)

    if start and end:
        return start, end

    raise ValueError("Start or end point not found in the maze.")

def optimized_flooding_search(binary_img, start, end):
    """Uses BFS (Flood Fill) to find the shortest path from start to end."""
    rows, cols = binary_img.shape
    neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up

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

    return came_from  # May be empty if no path exists

def reconstruct_path(came_from, start, end):
    """Reconstructs the shortest path from the BFS search result."""
    path = []
    current = end
    while current != start:
        path.append(current)
        current = came_from.get(current)
        if current is None:
            return []  # No valid path found
    path.append(start)
    path.reverse()
    return path

def optimized_visualize_maze(binary_img, path, explored, path_thickness=3):
    """Visualizes the solved maze with the path and explored cells."""
    color_img = np.zeros((*binary_img.shape, 3), dtype=np.uint8)
    color_img[binary_img == 255] = [255, 255, 255]  # White paths
    color_img[binary_img == 0] = [0, 0, 0]  # Black walls

    if explored:
        explored = np.array(explored)
        color_img[explored[:, 0], explored[:, 1]] = [255, 0, 0]  # Mark explored cells in red

    # Create a separate mask for the path and draw the path in green with thickness
    path_img = np.zeros(binary_img.shape, dtype=np.uint8)
    for r, c in path:
        path_img[r, c] = 255

    # Use OpenCV to thicken the path
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (path_thickness, path_thickness))
    thick_path = cv2.dilate(path_img, kernel)

    color_img[thick_path > 0] = [0, 255, 0]  # Draw the thick green path

    return color_img

def main():
    """Main function to load, process, solve, and visualize the maze."""
    print("Please select a maze image.")
    img_path = select_image()

    print(f"Processing: {os.path.basename(img_path)}")
    binary_img = preprocess_image(img_path)

    try:
        start, end = find_start_end(binary_img)
    except ValueError as e:
        print(f"Error: {e}")
        return

    print("Solving the maze...")
    st_time = time()
    came_from = optimized_flooding_search(binary_img, tuple(start), tuple(end))
    if not came_from:
        print("No solution found.")
        return

    path = reconstruct_path(came_from, tuple(start), tuple(end))
    explored = list(came_from.keys())
    print(f"Solved in {time() - st_time:.2f} seconds.")

    print("Visualizing the solution...")
    result_img = optimized_visualize_maze(binary_img, path, explored)

    output_path = os.path.join(os.path.dirname(img_path), "solved_" + os.path.basename(img_path))
    PIL.Image.fromarray(result_img).save(output_path)
    print(f"Solution saved as {output_path}")

if __name__ == "__main__":
    main()
