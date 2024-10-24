from ClassFiles.MainController import MainController

def main():
    # Specify the CSV file path for the discrete system matrices
    input_file = './DATA/plant_system_discrete_matrices.csv'

    # Create an instance of MainController
    main_controller = MainController(input_file)

    # Start the slider control
    main_controller.slider_controller.start()

if __name__ == '__main__':
    main()
