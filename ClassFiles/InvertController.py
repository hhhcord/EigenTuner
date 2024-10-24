import tkinter as tk
import numpy as np

class InvertController:
    def __init__(self, state_space_model, update_callback):
        """
        Initialize the invert controller with the given state-space model and 
        update callback function.
        """
        self.state_space_model = state_space_model
        self.update_callback = update_callback

        self.invert_window = None
        self.init_invert_window()

    def init_invert_window(self):
        """
        Create a separate window for Invert switches to control the sign of 
        each element in the feedback matrix.
        """
        self.invert_window = tk.Toplevel()
        self.invert_window.title("Invert Switch Control")

        self.num_rows, self.num_cols = self.state_space_model.feedback_matrix.shape

        # Add Invert switches for each element in the feedback matrix
        self.invert_switches = []
        for i in range(self.num_rows):
            row_invert_switches = []
            for j in range(self.num_cols):
                N = 8
                col_pos = j % N  # Column position for grid layout
                row_pos = i * (self.num_cols // N + 1) + (j // N) + 1  # Row position for grid layout

                # Create a switch for sign control
                sign_var = tk.IntVar(value=0)  # 0: positive, 1: inverted
                invert_switch = tk.Checkbutton(
                    self.invert_window,
                    text=f"F[{i}, {j}] Invert",
                    variable=sign_var,
                    command=lambda row=i, col=j, sign=sign_var: self.toggle_sign(row, col, sign)
                )
                invert_switch.grid(row=row_pos, column=col_pos, padx=5, pady=5)
                row_invert_switches.append(invert_switch)

            self.invert_switches.append(row_invert_switches)

    def toggle_sign(self, row, col, sign_var):
        """
        Toggle the sign of the feedback matrix element based on the Invert switch.
        """
        current_value = self.state_space_model.feedback_matrix[row, col]
        if sign_var.get() == 1:
            # If the switch is checked, invert the sign
            self.state_space_model.feedback_matrix[row, col] = -abs(current_value)
        else:
            # If the switch is unchecked, make the value positive
            self.state_space_model.feedback_matrix[row, col] = abs(current_value)

        # Call the update callback function to refresh the eigenvalue plot
        self.update_callback()
