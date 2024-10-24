import tkinter as tk
import numpy as np

class SliderController:
    def __init__(self, state_space_model, update_callback):
        """
        Initialize the slider controller with the given state-space model and 
        update callback function.
        """
        self.MAX = 36
        self.state_space_model = state_space_model
        self.update_callback = update_callback

        # Adjust number of rows and columns for the feedback matrix layout
        self.num_rows, self.num_cols = self.state_space_model.feedback_matrix.shape
        self.sliders = []

        self.init_sliders()

    def init_sliders(self):
        """
        Initialize sliders in a grid layout to control the elements of the 
        feedback matrix.
        """
        self.root = tk.Tk()
        self.root.title("Feedback Matrix Slider Control")

        # Add sliders for each element in the feedback matrix
        for i in range(self.num_rows):
            row_sliders = []
            for j in range(self.num_cols):
                N = 15
                col_pos = j % N  # Column position for grid layout
                row_pos = i * (self.num_cols // N + 1) + (j // N) + 1  # Row position for grid layout

                # Create sliders with logarithmic scaling
                slider = tk.Scale(
                    self.root,
                    from_=-self.MAX, to=self.MAX,  # dB range from -36 to 36
                    resolution=0.1,    # Set slider resolution
                    orient='horizontal',
                    length=90,
                    label=f'F[{i}, {j}]',
                    command=lambda val, row=i, col=j: self.update_feedback_matrix(row, col, float(val))
                )
                slider.grid(row=row_pos, column=col_pos, padx=5, pady=5)
                row_sliders.append(slider)

            self.sliders.append(row_sliders)

    def update_feedback_matrix(self, row, col, db_value):
        """
        Update the feedback matrix based on slider input.
        """
        # Convert dB value to linear scale
        linear_value = 10 ** (db_value / 20)

        # Apply the current sign of the element
        current_value = self.state_space_model.feedback_matrix[row, col]
        current_sign = -1 if current_value < 0 else 1
        new_feedback_matrix = np.copy(self.state_space_model.feedback_matrix)
        new_feedback_matrix[row, col] = linear_value * current_sign
        self.state_space_model.update_feedback_matrix(new_feedback_matrix)

        # Call the update callback function to refresh the eigenvalue plot
        self.update_callback()

    def display_feedback_element(self, row, col):
        """
        Display and update the slider value, highlighting it in green.
        """
        value = self.state_space_model.feedback_matrix[row, col]

        # Avoid taking log of zero by setting dB value to a minimum threshold
        if value == 0:
            db_value = -self.MAX  # Set to minimum dB value (or another appropriate value)
        else:
            db_value = 20 * np.log10(abs(value))  # Convert to dB scale

        slider = self.sliders[row][col]
        slider.set(db_value)
        slider.config(bg='green')

    def highlight_slider(self, row, col, highlight=True):
        """
        Highlight a specific slider, usually to indicate an error.
        """
        slider = self.sliders[row][col]
        if highlight:
            slider.config(bg='red')
        else:
            slider.config(bg='SystemButtonFace')

    def start(self):
        """
        Start the Tkinter main loop to display the GUI.
        """
        self.root.mainloop()
