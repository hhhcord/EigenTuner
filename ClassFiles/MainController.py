import os
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ClassFiles.StateSpaceModel import StateSpaceModel
from ClassFiles.EigenvalueMonitor import EigenvalueMonitor
from ClassFiles.SliderController import SliderController
from ClassFiles.InvertController import InvertController  # New import for Invert Window
from ClassFiles.WarningSystem import WarningSystem
from ClassFiles.FileHandler import FileHandler

class MainController:
    def __init__(self, input_file):
        self.root = tk.Tk()
        self.root.title("Eigenvalue Tuner")
        
        # Load matrices from the CSV file
        self.file_handler = FileHandler()
        self.file_handler.load_matrices_from_csv(input_file)
        
        # Initialize subsystems
        self.state_space_model = StateSpaceModel(self.file_handler.A, self.file_handler.B)
        self.slider_controller = SliderController(self.state_space_model, self.update_view)
        self.invert_controller = InvertController(self.state_space_model, self.update_view)  # New Invert controller
        self.eigen_monitor = EigenvalueMonitor(self.state_space_model)
        self.warning_system = WarningSystem(self.slider_controller)

        # Initialize UI
        self.init_ui()

    def init_ui(self):
        """Initialize the main user interface"""
        # Place the Save button at the top-left corner (row=0, column=0)
        self.save_button = tk.Button(
            self.slider_controller.root,
            text="Save Gain Matrix",
            command=self.save_gain
        )
        self.save_button.grid(row=0, column=0, pady=10, sticky='nw')
        # Embed the figure in Tkinter Canvas
        self.fig = self.eigen_monitor.fig
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas.draw()

    def update_view(self):
        """Update the eigenvalues visualization based on state space model changes"""
        self.eigen_monitor.update_eigenvalues()
        self.warning_system.check_stability()

    def save_gain(self):
        """Save the gain matrix to a CSV file"""
        output_dir = './output'
        output_file = 'gain.csv'

        # Create the output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Save the gain matrix
        gain_matrix = self.state_space_model.feedback_matrix
        self.file_handler.save_matrix(gain_matrix, os.path.join(output_dir, output_file))
