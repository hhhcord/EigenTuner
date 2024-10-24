import numpy as np
import pandas as pd
import ast

class ControllerGainGenerator:
    def __init__(self, system_order):
        """
        Initializes the ControllerGainGenerator class with the given system order.

        Parameters:
        system_order (int): The order of the control system.
        """
        self.system_order = system_order

    def generate_initial_controller_gain(self, lower_bound=-5e-2, upper_bound=5e-2):
        """
        Generates the initial controller gain based on the specified system order.
        
        Parameters:
        lower_bound (float): Lower bound of the random values (default is -5e-2).
        upper_bound (float): Upper bound of the random values (default is 5e-2).

        Returns:
        np.array: A random array representing the initial controller gain.
        """
        # Generate random values within the specified range
        return np.random.uniform(lower_bound, upper_bound, size=self.system_order)

    def load_state_feedback_gain(self, file_path='output/gain.csv'):
        """
        Reads the state feedback gain F from a CSV file and returns it as a NumPy array.

        Parameters:
        file_path (str): The path to the gain.csv file (default is 'output/gain.csv').

        Returns:
        np.array: State feedback gain F as a NumPy array.
        """
        # Read the CSV file
        gain_df = pd.read_csv(file_path)

        # Extract the 'Values' column from the 'State Feedback Gain (F)' row
        gain_values_str = gain_df[gain_df['Gain Type'] == 'State Feedback Gain (F)']['Values'].values[0]

        # Convert the string representation of the list to an actual list
        state_feedback_gain_list = ast.literal_eval(gain_values_str)

        # Convert the list to a NumPy array
        state_feedback_gain_array = np.array(state_feedback_gain_list)

        return state_feedback_gain_array

    def main(self):
        """
        Orchestrates the process of generating initial controller gain and 
        loading the state feedback gain.

        Returns:
        tuple: Initial controller gain and state feedback gain array.
        """
        # Generate initial controller gain
        initial_controller_gain = self.generate_initial_controller_gain()

        # Load state feedback gain from CSV
        state_feedback_gain_array = self.load_state_feedback_gain()

        return initial_controller_gain, state_feedback_gain_array

# Example usage
if __name__ == "__main__":
    # Define the system order
    system_order = 4  # Example order

    # Instantiate the class
    controller = ControllerGainGenerator(system_order)

    # Get the gains
    initial_gain, state_feedback_gain = controller.main()

    # Print the results
    print("Initial Controller Gain:", initial_gain)
    print("State Feedback Gain Array:", state_feedback_gain)
