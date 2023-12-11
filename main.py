import tkinter as tk  # Import the tkinter library for GUI creation
from config import DEFAULT_COLORS, BUTTON_CONFIG  # Import configurations from external files
from registration_logging import LoggingInterface  # Import the LoggingInterface class

def start_logging():
    """
    Function to initiate the logging process.
    Initializes the root window, configuration settings, and LoggingInterface instance.
    """
    root = tk.Tk()  # Initialize the main Tkinter window
    config = {
        'button_width_ratio': 0.01,  # Ratio for button width in relation to screen width
        'button_height_ratio': 0.004,  # Ratio for button height in relation to screen height
        **DEFAULT_COLORS  # Includes default colors from the config
    }
    logging = LoggingInterface(root, config)  # Create an instance of LoggingInterface
    root.mainloop()  # Start the Tkinter event loop for the GUI

if __name__ == "__main__":
    start_logging()  # Call the function to start the logging process
