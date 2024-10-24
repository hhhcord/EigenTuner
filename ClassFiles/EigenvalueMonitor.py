import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

class EigenvalueMonitor:
    def __init__(self, state_space_model):
        self.state_space_model = state_space_model
        self.fig, self.ax = plt.subplots()
        self.eigenvalue_markers = []

        # Initial plot settings
        self.ax.set_xlabel('Real Part')
        self.ax.set_ylabel('Imaginary Part [Hz]')
        self.ax.set_xlim(-1e6, 1e3)  # Set X-axis range
        self.ax.set_ylim(-48e3, 48e3)  # Set Y-axis range

        # Add grid for better visualization
        self.ax.grid(which='both', linestyle='-', linewidth='0.8', color='gray')

        # Set X-axis to symlog scale with appropriate linthresh for real part
        self.ax.set_xscale('symlog', linthresh=10)
        self.ax.xaxis.set_major_locator(ticker.SymmetricalLogLocator(base=10, linthresh=10))
        self.ax.xaxis.set_major_formatter(ticker.FuncFormatter(self.custom_formatter))

        # Set Y-axis to symlog scale with appropriate linthresh for imaginary part
        self.ax.set_yscale('symlog', linthresh=10)
        self.ax.yaxis.set_major_locator(ticker.SymmetricalLogLocator(base=2, linthresh=10))
        self.ax.yaxis.set_major_formatter(ticker.FuncFormatter(self.custom_formatter))

    def custom_formatter(self, y, pos):
        """Custom formatter for axis labels, displaying in kHz where appropriate."""
        abs_y = np.abs(y)
        if abs_y >= 1e3:
            return f'{abs_y/1e3:.1f}k'
        else:
            return f'{abs_y:.0f}'

    def update_eigenvalues(self):
        """Update and plot eigenvalues in real-time."""
        eigenvalues = self.state_space_model.calculate_eigenvalues()

        # Remove existing markers if present
        for marker in self.eigenvalue_markers:
            marker.remove()

        self.eigenvalue_markers.clear()

        # Calculate real and imaginary parts
        real_parts = np.real(eigenvalues)
        # imag_parts = np.imag(eigenvalues)
        # Update y-axis values to scale by 2*pi
        imag_parts = np.imag(eigenvalues) / (2 * np.pi)

        # Plot each eigenvalue with appropriate color
        for real, imag in zip(real_parts, imag_parts):
            color = 'green' if real < 0 else 'red'  # Green for negative, red for positive real part
            marker, = self.ax.plot(real, imag, 'x', markersize=10, color=color)
            self.eigenvalue_markers.append(marker)

        self.fig.canvas.draw()

    def show_plot(self):
        """Display the plot."""
        plt.tight_layout()
        plt.show(block=False)
