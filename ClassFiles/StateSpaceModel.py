import numpy as np
import scipy.linalg

class StateSpaceModel:
    def __init__(self, system_matrix, input_matrix, sampling_period=44.1e3):
        """
        Initialize the state-space model with system matrix A, input matrix B, 
        and sampling period.
        """
        self.system_matrix = system_matrix  # A matrix
        self.input_matrix = input_matrix  # B matrix
        self.feedback_matrix = np.zeros((input_matrix.shape[1], system_matrix.shape[0]))  # Initialize F matrix
        self.sampling_period = sampling_period  # Sampling period

    def update_feedback_matrix(self, new_feedback_matrix):
        """
        Update the feedback matrix F and recalculate (A - BF).
        """
        self.feedback_matrix = new_feedback_matrix

    def get_discrete_A_BF(self):
        """
        Calculate the discrete-time state-space matrix (A - BF).
        """
        return self.system_matrix - self.input_matrix @ self.feedback_matrix

    def get_continuous_A_BF(self):
        """
        Convert the discrete-time matrix (A - BF) to a continuous-time matrix.
        """
        discrete_A_BF = self.get_discrete_A_BF()
        # print('\ndiscrete_A_BF: ', discrete_A_BF)

        dt = self.calculate_control_period(self.sampling_period)

        # Calculate the continuous-time matrix using the matrix logarithm
        continuous_A_BF = scipy.linalg.logm(discrete_A_BF) / dt
                
        return continuous_A_BF

    def calculate_eigenvalues(self):
        """
        Calculate the eigenvalues of the continuous-time matrix (A - BF).
        """
        continuous_A_BF = self.get_continuous_A_BF()
        eigenvalues = np.linalg.eigvals(continuous_A_BF)
        return eigenvalues
    
    def calculate_control_period(self, sampling_frequency):
        """
        Calculate the control period (sampling period) from the sampling frequency (in Hz).
        """
        return 1.0 / sampling_frequency
