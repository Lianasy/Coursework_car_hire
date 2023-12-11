import tkinter as tk
from config import DEFAULT_COLORS, BUTTON_CONFIG

class UserInterface:
    def __init__(self, root, login, password):
        """
        Initialize the UserInterface class with the given parameters.

        Args:
        - root (tk.Tk): The root window object
        - login (str): User login information
        - password (str): User password information
        """
        self.root = root  # Reference to the main Tkinter window
        self.screen_width = self.root.winfo_screenwidth()  # Get the screen width
        self.screen_height = self.root.winfo_screenheight()  # Get the screen height

        self.create_interface()  # Call the method to create the user interface

    def create_interface(self):
        """
        Create the user interface with labels, buttons, and configurations.
        """
        self.root.title("User Interface")  # Set the title of the window
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")  # Set window size
        self.root.configure(bg=DEFAULT_COLORS['background_color'])  # Set background color

        # Create a label welcoming the user to the interface
        welcome_label = tk.Label(
            self.root,
            text="Welcome to User Interface!",
            font=('Arial', 24),
            bg=DEFAULT_COLORS['background_color']
        )
        welcome_label.pack(pady=20)  # Place the label in the window with padding

        # Create a logout button that triggers the logout method when clicked
        logout_button = tk.Button(
            self.root,
            text="Logout",
            command=self.logout,  # Set the command to call the logout method
            width=20,
            height=2,
            bg=DEFAULT_COLORS['button_color_1']
        )
        logout_button.pack(pady=10)  # Place the button in the window with padding

    def logout(self):
        """
        Logout function to close the user interface window.
        """
        self.root.destroy()  # Close the window of the user interface
