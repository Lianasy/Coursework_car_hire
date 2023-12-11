import tkinter as tk  # Import the Tkinter library for GUI creation
from UserInterface import *  # Import the UserInterface class from UserInterface module
from config import DEFAULT_COLORS, BUTTON_CONFIG  # Import default colors and button configurations

class LoggingInterface:
    def __init__(self, root, config):
        """
        Initialize the LoggingInterface class with the given parameters.

        Args:
        - root (tk.Tk): The root window object
        - config (dict): Configuration dictionary containing button dimensions and colors
        """
        self.root = root  # Reference to the main Tkinter window
        self.screen_width = self.root.winfo_screenwidth()  # Get the screen width
        self.screen_height = self.root.winfo_screenheight()  # Get the screen height

        # Calculate button dimensions based on screen size and provided ratios from the config
        self.btn_width = int(self.screen_width * config['button_width_ratio'])
        self.btn_height = int(self.screen_height * config['button_height_ratio'])

        self.entry_login = None  # Initialize user login entry field
        self.entry_password = None  # Initialize user password entry field
        self.button_config = BUTTON_CONFIG  # Assign button configuration from imported constants

        self.create_interface(config)  # Call the method to create the login interface with provided config

    def create_interface(self, config):
        """
        Create the login interface with buttons, labels, and entry fields based on the provided configuration.
        """
        self.root.title("Login System")  # Set the title of the window
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")  # Set window size
        self.root.configure(bg=config['background_color'])  # Set background color

        # Create 'Login as User' button
        btn_user = tk.Button(
            self.root,
            text="Login as User",
            command=self.logging_user,
            width=int(self.screen_width * self.button_config['user']['button_width_ratio']),
            height=int(self.screen_height * self.button_config['user']['button_height_ratio']),
            bg=config['button_color_1']
        )
        btn_user.place(relx=self.button_config['user']['relx'], rely=self.button_config['user']['rely'], anchor=tk.CENTER)

        # Create 'Login as Employee' button
        btn_employee = tk.Button(
            self.root,
            text="Login as Employee",
            command=self.logging_employee,
            width=int(self.screen_width * self.button_config['employee']['button_width_ratio']),
            height=int(self.screen_height * self.button_config['employee']['button_height_ratio']),
            bg=config['button_color_2']
        )
        btn_employee.place(relx=self.button_config['employee']['relx'], rely=self.button_config['employee']['rely'], anchor=tk.CENTER)

    def clear_interface(self):
        """
        Clear all widgets (buttons, labels, etc.) from the root window.
        """
        for widget in self.root.winfo_children():
            widget.destroy()

    def logging_user(self):
        """
        Display elements for user login (sign in and sign up) upon 'Login as User' button click.
        """
        # Clear the interface
        self.clear_interface()

        # Create 'Sign in' button
        btn_login = tk.Button(
            self.root,
            text="Sign in",
            command=self.login_account,
            width=self.btn_width,
            height=self.btn_height,
            bg=DEFAULT_COLORS['button_color_1']
        )
        btn_login.place(relx=self.button_config['login_button']['relx'], rely=self.button_config['login_button']['rely'], anchor=tk.CENTER)

        # Create 'Sign up' button
        btn_register = tk.Button(
            self.root,
            text="Sign up",
            command=self.create_account,
            width=self.btn_width,
            height=self.btn_height,
            bg=DEFAULT_COLORS['button_color_2']
        )
        btn_register.place(relx=self.button_config['register_button']['relx'], rely=self.button_config['register_button']['rely'], anchor=tk.CENTER)

    def logging_employee(self):
        """
        Display elements for employee login (login and password fields) upon 'Login as Employee' button click.
        """
        # Clear the interface
        self.clear_interface()

        # Create 'Enter login' label
        lbl_login = tk.Label(
            self.root,
            text="Enter login",
            bg=DEFAULT_COLORS['background_color']
        )
        lbl_login.place(relx=self.button_config['login_label']['relx'], rely=self.button_config['login_label']['rely'], anchor=tk.CENTER)

        # Create entry field for login
        self.entry_login = tk.Entry(
            self.root,
            width=int(self.btn_width * 1.5)
        )
        self.entry_login.place(relx=self.button_config['login_entry']['relx'], rely=self.button_config['login_entry']['rely'], anchor=tk.CENTER)

        # Create 'Enter password' label
        lbl_password = tk.Label(
            self.root,
            text="Enter password",
            bg=DEFAULT_COLORS['background_color']
        )
        lbl_password.place(relx=self.button_config['password_label']['relx'], rely=self.button_config['password_label']['rely'], anchor=tk.CENTER)

        # Create entry field for password
        self.entry_password = tk.Entry(
            self.root,
            width=int(self.btn_width * 1.5),
            show="*"
        )
        self.entry_password.place(relx=self.button_config['password_entry']['relx'], rely=self.button_config['password_entry']['rely'], anchor=tk.CENTER)

        # Create 'Sign in' button
        btn_login = tk.Button(
            self.root,
            text="Sign in",
            command=self.login_employee_account,
            width=self.btn_width,
            height=self.btn_height,
            bg=DEFAULT_COLORS['button_color_1']
        )
        btn_login.place(relx=self.button_config['sign_in_button']['relx'], rely=self.button_config['sign_in_button']['rely'], anchor=tk.CENTER)

    def login_account(self):
        """
        Display elements for logging in with a username and password upon 'Sign in' button click.
        """
        # Clear the interface
        self.clear_interface()

        # Create 'Enter login' label
        lbl_login = tk.Label(
            self.root,
            text="Enter login",
            bg=DEFAULT_COLORS['background_color']
        )
        lbl_login.place(relx=self.button_config['login_label']['relx'], rely=self.button_config['login_label']['rely'], anchor=tk.CENTER)

        # Create entry field for login
        self.entry_login = tk.Entry(
            self.root,
            width=int(self.btn_width * 1.5)
        )
        self.entry_login.place(relx=self.button_config['login_entry']['relx'], rely=self.button_config['login_entry']['rely'], anchor=tk.CENTER)

        # Create 'Enter password' label
        lbl_password = tk.Label(
            self.root,
            text="Enter password",
            bg=DEFAULT_COLORS['background_color']
        )
        lbl_password.place(relx=self.button_config['password_label']['relx'], rely=self.button_config['password_label']['rely'], anchor=tk.CENTER)

        # Create entry field for password
        self.entry_password = tk.Entry(
            self.root,
            width=int(self.btn_width * 1.5),
            show="*"
        )
        self.entry_password.place(relx=self.button_config['password_entry']['relx'], rely=self.button_config['password_entry']['rely'], anchor=tk.CENTER)

        # Create 'Sign In' button
        btn_login = tk.Button(
            self.root,
            text="Sign In",
            command=self.process_login,
            width=self.btn_width,
            height=self.btn_height,
            bg=DEFAULT_COLORS['button_color_1']
        )
        btn_login.place(relx=self.button_config['sign_in_button']['relx'], rely=self.button_config['sign_in_button']['rely'], anchor=tk.CENTER)

    def create_account(self):
        """
        Display elements for creating a new account upon 'Sign up' button click.
        """
        # Clear the interface
        self.clear_interface()

        # Create 'Enter new login' label
        lbl_login = tk.Label(
            self.root,
            text="Enter new login",
            bg=DEFAULT_COLORS['background_color']
        )
        lbl_login.place(relx=self.button_config['login_label']['relx'], rely=self.button_config['login_label']['rely'], anchor=tk.CENTER)

        # Create entry field for new login
        self.entry_login = tk.Entry(
            self.root,
            width=int(self.btn_width * 1.5)
        )
        self.entry_login.place(relx=self.button_config['login_entry']['relx'], rely=self.button_config['login_entry']['rely'], anchor=tk.CENTER)

        # Create 'Enter new password' label
        lbl_password = tk.Label(
            self.root,
            text="Enter new password",
            bg=DEFAULT_COLORS['background_color']
        )
        lbl_password.place(relx=self.button_config['password_label']['relx'], rely=self.button_config['password_label']['rely'], anchor=tk.CENTER)

        # Create entry field for new password
        self.entry_password = tk.Entry(
            self.root,
            width=int(self.btn_width * 1.5),
            show="*"
        )
        self.entry_password.place(relx=self.button_config['password_entry']['relx'], rely=self.button_config['password_entry']['rely'], anchor=tk.CENTER)

        # Create 'Sign Up' button
        btn_create = tk.Button(
            self.root,
            text="Sign Up",
            command=self.process_signup,
            width=self.btn_width,
            height=self.btn_height,
            bg=DEFAULT_COLORS['button_color_2']
        )
        btn_create.place(relx=self.button_config['sign_up_button']['relx'], rely=self.button_config['sign_up_button']['rely'], anchor=tk.CENTER)

    def process_login(self):
        """
        Process the login by retrieving login and password information, print them, and display the user interface.
        """
        login = self.entry_login.get()
        password = self.entry_password.get()
        print(f"Logging in with Login: {login}, Password: {password}")
        self.show_user_interface(login, password)

    def show_user_interface(self, login, password):
        """
        Display the user interface using the UserInterface class instance in the same window.
        """
        self.clear_interface()  # Clear the previous interface

        # Create an instance of the UserInterface class to display the user interface in the same window
        user_interface = UserInterface(self.root, login=login, password=password)

    def logout(self):
        """
        Log out the user by clearing the interface and displaying the login interface again.
        """
        self.clear_interface()  # Clear the user interface
        self.create_interface()  # Show the login interface again

    def process_signup(self):
        """
        Process the creation of a new account by retrieving login and password information and printing them.
        """
        new_login = self.entry_login.get()
        new_password = self.entry_password.get()
        print(f"Creating new account with Login: {new_login}, Password: {new_password}")

    def login_employee_account(self):
        """
        Check if login and password fields exist, retrieve information, and print them for employee login.
        """
        if self.entry_login and self.entry_password:
            login = self.entry_login.get()
            password = self.entry_password.get()
            print(f"Login: {login}, Password: {password}")
        else:
            print("Login and password fields are not created")



