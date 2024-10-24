import csv
import numpy as np
import pandas as pd

class FileHandler:
    def __init__(self, n=2):
        """
        Initialize the matrix handler with a given degree n.

        Args:
            n (int): The degree used to determine the matrix reading positions.
        """
        self.n = n
        self.A = None
        self.B = None
        self.C = None
        self.D = None

    def load_matrices_from_csv(self, filename):
        """
        Load state-space matrices A, B, C, D from a CSV file.

        Args:
            filename (str): The path to the CSV file containing the matrices.
        """
        try:
            # Initialize lists to collect matrix data
            a_rows, b_rows, c_rows, d_rows = [], [], [], []
            current_matrix = None

            # Open the CSV file and read its contents
            with open(filename, 'r') as csvfile:
                reader = csv.reader(csvfile)

                for row in reader:
                    # Identify the matrix type based on the first element
                    if row[0] == 'A':
                        current_matrix = 'A'
                    elif row[0] == 'B':
                        current_matrix = 'B'
                    elif row[0] == 'C':
                        current_matrix = 'C'
                    elif row[0] == 'D':
                        current_matrix = 'D'
                    elif row[0] and current_matrix:  # If the row is not empty and a matrix is specified
                        try:
                            # Add row data to the appropriate matrix list
                            values = list(map(float, row))
                            if current_matrix == 'A':
                                a_rows.append(values)
                            elif current_matrix == 'B':
                                b_rows.append(values)
                            elif current_matrix == 'C':
                                c_rows.append(values)
                            elif current_matrix == 'D':
                                d_rows.append(values)
                        except ValueError:
                            # Skip rows that cannot be converted to floats
                            continue

            # Convert lists to numpy arrays and assign them to matrix attributes
            self.A = np.array(a_rows) if a_rows else None
            self.B = np.array(b_rows) if b_rows else None
            self.C = np.array(c_rows) if c_rows else None
            self.D = np.array(d_rows) if d_rows else None

            print(f"Matrices loaded from {filename}")

        except FileNotFoundError:
            print(f"File not found: {filename}")
        except Exception as e:
            print(f"Error loading matrices from {filename}: {e}")

    def save_matrix(self, gain, file_path):
        """
        Save gain data to a CSV file in a specific format.

        Args:
            gain (np.ndarray): The gain data to be saved.
            file_path (str): The path to the CSV file.
        """
        try:
            # Prepare gain data in the required format
            gain_data = {
                "Gain Type": ["State Feedback Gain (F)"],
                "Continuous/Discrete": ["Discrete"],
                "Values": [f"[{', '.join(map(str, gain.flatten()))}]"]
            }
            gain_df = pd.DataFrame(gain_data)

            # Save gain data to CSV
            gain_df.to_csv(file_path, index=False)
            print(f"Gain saved to {file_path}")

        except Exception as e:
            print(f"Error saving gain to {file_path}: {e}")
