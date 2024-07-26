import tkinter as tk
from tkinter import Tk, Label, Canvas, Frame
import re

# Function to read the results from the VisualPrediction.txt file
def read_results(filename='VisualPrediction.txt'):
    results = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                match = re.search(r"label: '(.*?)', value: ([\d.]+)", line)
                if match:
                    label = match.group(1)
                    value = float(match.group(2))
                    results.append({'label': label, 'value': value})
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")

    return results

# Function to find the label with the highest value
def find_highest_label(results):
    if not results:
        return None

    highest_label = max(results, key=lambda x: x['value'])
    return highest_label['label']

# Function to create a simple GUI based on the results
def create_gui(results):
    if not results:
        return

    root = Tk()
    root.title("Visual Prediction Results")

    # Specify the number of columns in the grid
    num_columns = 10

    # Calculate the number of rows needed based on the total number of results
    num_results = len(results)
    num_rows = (num_results + num_columns - 1) // num_columns

    # Define a scaling factor for the bar height and container height
    bar_height_scale = 1.0
    container_height_scale = 1.0  # Adjusted scaling factor for the container height

    # Poppins font for labels
    font_poppins = ("Poppins", 10)  # Adjust the size as needed

    for index, result in enumerate(results):
        label = result.get('label', '')
        value = result.get('value', 0.0)

        # Calculate row and column for each label and its value bar
        row_index = index // num_columns
        col_index = index % num_columns

        # Create a frame for each label
        frame = Frame(root, padx=5, pady=5)
        frame.grid(row=row_index, column=col_index, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create a label to display the name of the label with Poppins font
        label_widget = Label(frame, text=label, font=font_poppins)
        label_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create a canvas to draw the color-filled box based on the value
        canvas = Canvas(frame, width=30, height=100 * container_height_scale, background='white')
        canvas.grid(row=1, column=0)

        # Calculate the height of the filled rectangle based on the value
        filled_height = int(value * 100 * bar_height_scale * container_height_scale)  # Adjusted canvas height

        # Calculate the y-coordinate for starting the filled rectangle at the bottom
        y_coord = 100 * container_height_scale - filled_height

        # Draw the filled rectangle vertically, starting at the bottom
        canvas.create_rectangle(0, y_coord, 30, 100 * container_height_scale, fill='red')

        # Configure the column to center the canvas in the frame
        frame.columnconfigure(0, weight=1)

    # Find the label with the highest value
    highest_label = find_highest_label(results)

    # Poppins font for the message label
    font_poppins_bold = ("Poppins", 12, "bold")  # Adjust the size and weight as needed

    # Create and display the label for executing voice command directly in the grid
    execution_label = Label(root, text=f"Executing voice command: {highest_label}", font=font_poppins_bold)
    execution_label.grid(row=num_rows, column=0, columnspan=num_columns, sticky=tk.W)

    root.mainloop()

# Main function
def main():
    # Read the results from the VisualPrediction.txt file
    results = read_results()

    # Create the GUI based on the results
    create_gui(results)

if __name__ == "__main__":
    main()
