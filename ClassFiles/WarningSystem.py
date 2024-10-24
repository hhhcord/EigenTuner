import numpy as np

class WarningSystem:
    def __init__(self, slider_controller):
        self.slider_controller = slider_controller

    def check_stability(self):
        """ Check the eigenvalues of (A - BF) and highlight sliders accordingly. """
        
        # Calculate eigenvalues of the state-space model
        eigenvalues = self.slider_controller.state_space_model.calculate_eigenvalues()

        # Find indices of unstable eigenvalues (real part > 0)
        unstable_indices = np.where(np.real(eigenvalues) > 0)[0]

        # Reset all slider highlights initially
        for row in range(self.slider_controller.num_rows):
            for col in range(self.slider_controller.num_cols):
                self.slider_controller.highlight_slider(row, col, highlight=False)

        # If any unstable eigenvalues are found, highlight the related F elements
        if unstable_indices.size > 0:
            for row in range(self.slider_controller.num_rows):
                for col in range(self.slider_controller.num_cols):
                    self.slider_controller.highlight_slider(row, col, highlight=True)
        else:
            # Ensure F elements are shown even when no unstable eigenvalues are found
            for row in range(self.slider_controller.num_rows):
                for col in range(self.slider_controller.num_cols):
                    self.slider_controller.display_feedback_element(row, col)
