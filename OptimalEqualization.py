import copy
from ClassFiles.AudioLoader import AudioLoader  # Import the AudioLoader class
from ClassFiles.FrequencyResponseAnalyzer import FrequencyResponseAnalyzer  # Import the FrequencyResponseAnalyzer class
from ClassFiles.ControlSystemSimulation import ControlSystemSimulation
from ClassFiles.StateFeedbackControllerSimulation import StateFeedbackController
from ClassFiles.ControllerGainGenerator import ControllerGainGenerator

def main():
    # Create an instance of AudioLoader
    print("Creating AudioLoader instance...")
    al = AudioLoader()

    # Specify the duration in seconds to read
    time_test = 20  # Time duration for input/output audio data
    time_input = 20  # Time duration for test audio data
    # time_input = 27
    # time_input = 254

    # Load the input audio signal for a specified time period
    print("\nPlease select the .wav file for the input audio signal")
    input_data, sampling_rate = al.load_audio(time_test)
    print("Input audio signal loaded.")

    # Load the output audio signal for the same time period
    print("\nPlease select the .wav file for the output audio signal")
    output_data, _ = al.load_audio(time_test)
    print("Output audio signal loaded.")

    # Load the test audio signal for a different time period
    print("\nPlease select the .wav file for the test audio signal")
    test_data, _ = al.load_audio(time_input)
    print("Test audio signal loaded.")

    # Create an instance of FrequencyResponseAnalyzer and perform analysis
    print("Creating FrequencyResponseAnalyzer instance and analyzing frequency response...")
    fra = FrequencyResponseAnalyzer(input_signal=input_data, output_signal=output_data, sampling_rate=sampling_rate, time_duration=time_test)
    fra.analyze_and_save_bode_plot()
    print("Frequency response analysis completed and Bode plot saved.")

    # Specify the order of the system for simulation
    system_order = 149

    # Instantiate the class
    controller = ControllerGainGenerator(system_order)

    # Get the gains
    initial_gain, state_feedback_gain = controller.main()
    state_feedback_gain = state_feedback_gain.reshape(-1, 1)
    state_feedback_gain = state_feedback_gain.T

    # Print the results
    print("Initial Controller Gain:", initial_gain)
    print("State Feedback Gain Array:", state_feedback_gain)

    # Set up the control system simulation
    print("Setting up the control system simulation...")
    simulation = ControlSystemSimulation(n=system_order, t_end=time_test, num_points=len(input_data))

    # Plot the input and output signals
    print("Plotting input and output signals...")
    simulation.plot_input_output(input_data, output_data, filename='input_output_plot.png')

    # Identify the system using SRIM method
    print("Identifying system using SRIM method...")
    SRIM_plant_system = simulation.identify_system_SRIM(input_data, output_data)
    print("System identification completed.")

    # Create an independent copy of SRIM_plant_system
    print("Creating a deep copy of the SRIM_plant_system...")
    SRIM_ideal_system = copy.deepcopy(SRIM_plant_system)

    # Update the A matrix with state feedback control
    print("Updating the A matrix with state feedback gain...")
    SRIM_ideal_system.A = SRIM_ideal_system.A - SRIM_ideal_system.B @ state_feedback_gain

    print("Update complete.")

    # Plot the step response for the identified system
    print("Plotting step response for the identified system...")
    simulation.plot_step_response_PlantVsIdeal(SRIM_plant_system, SRIM_ideal_system)

    # Plot the eigenvalues for the identified system
    print("Plotting eigenvalues for the identified system...")
    simulation.plot_eigenvalues_PlantVsIdeal(SRIM_plant_system, SRIM_ideal_system)

    # Plot the Bode plot for the identified system
    print("Plotting Bode plot for the identified system...")
    simulation.plot_bode_PlantVsIdeal(SRIM_plant_system, SRIM_ideal_system)

    # Process the system matrix and save the natural frequencies
    print("Processing system matrix and saving natural frequencies...")
    simulation.process_matrix_and_save(SRIM_plant_system.A, filename="plant_system_eigenvalues_frequencies.csv")
    simulation.process_matrix_and_save(SRIM_ideal_system.A, filename="plant_system_eigenvalues_frequencies.csv")

    # Set up the State Feedback Controller
    print("Setting up State Feedback Controller...")
    SFC = StateFeedbackController(
        n=system_order, 
        plant_system=SRIM_plant_system, 
        ideal_system=SRIM_ideal_system, 
        input_signal=input_data, 
        test_signal=test_data, 
        sampling_rate=sampling_rate, 
        F_ini=initial_gain, 
        F_ast=state_feedback_gain
    )

    # Simulate the system and get the output signals
    print("Running the State Feedback Controller simulation...")
    uncontrolled_output, controlled_output, control_input_signal = SFC.optimal_equalization()
    print("Simulation completed.")

    # Save the resulting audio signals
    print("Saving the simulated output signals as audio files...")
    al.save_audio(uncontrolled_output, sampling_rate, 'UncontrolledOutput')
    al.save_audio(controlled_output, sampling_rate, 'ControlledOutput')
    al.save_audio(control_input_signal, sampling_rate, 'ControlInputSignal')
    print("All audio files saved.")

if __name__ == "__main__":
    main()
