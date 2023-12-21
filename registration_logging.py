import tkinter as tk  # Import the Tkinter library for GUI creation
import tkcalendar
import re

from CarHireInterface import CarHire
from UserInterface import *  # Import the UserInterface class from UserInterface module
from config import DEFAULT_COLORS, BUTTON_CONFIG  # Import default colors and button configurations
from Users import LogIn, Registration
import Users
import Controller
class LoggingInterface:
    def __init__(self, root, config):
        """
        Initialize the LoggingInterface class with the given parameters.

        Args:
        - root (tk.Tk): The root window object
        - config (dict): Configuration dictionary containing button dimensions and colors
        """
        self.entry_photo = None
        self.entry_lname = None
        self.entry_phone = None
        self.entry_licence = None
        self.entry_email = None
        self.entry_passport = None
        self.entry_license_number = None
        self.entry_birth_date = None
        self.entry_name = None
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
        self.logging_user()

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
        # Create 'Enter login' label
        lbl_login = tk.Label(
            self.root,
            text="Enter login",
            bg=DEFAULT_COLORS['background_color']
        )
        lbl_login.place(relx=self.button_config['login_label']['relx'], rely=self.button_config['login_label']['rely'],
                        anchor=tk.CENTER)

        # Create entry field for login
        self.entry_login = tk.Entry(
            self.root,
            width=int(self.btn_width * 1.5)
        )
        self.entry_login.place(relx=self.button_config['login_entry']['relx'],
                               rely=self.button_config['login_entry']['rely'], anchor=tk.CENTER)

        # Create 'Enter password' label
        lbl_password = tk.Label(
            self.root,
            text="Enter password",
            bg=DEFAULT_COLORS['background_color']
        )
        lbl_password.place(relx=self.button_config['password_label']['relx'],
                           rely=self.button_config['password_label']['rely'], anchor=tk.CENTER)

        # Create entry field for password
        self.entry_password = tk.Entry(
            self.root,
            width=int(self.btn_width * 1.5),
            show="*"
        )
        self.entry_password.place(relx=self.button_config['password_entry']['relx'],
                                  rely=self.button_config['password_entry']['rely'], anchor=tk.CENTER)

        # Create 'Sign In' button
        btn_login = tk.Button(
            self.root,
            text="Sign In",
            command=self.process_login,
            width=self.btn_width,
            height=self.btn_height,
            bg=DEFAULT_COLORS['button_color_1']
        )
        btn_login.place(relx=self.button_config['sign_in_button']['relx'],
                        rely=self.button_config['sign_in_button']['rely'], anchor=tk.CENTER)
        # Create 'Sign up' button
        btn_register = tk.Button(
            self.root,
            text="Sign up",
            command=self.create_account,
            width=self.btn_width,
            height=self.btn_height,
            bg=DEFAULT_COLORS['button_color_2']
        )
        btn_register.place(relx=self.button_config['sign_up_button']['relx'],
                           rely=self.button_config['sign_up_button']['rely'], anchor=tk.CENTER)

    def login_account(self):
        """
        Display elements for logging in with a username and password upon 'Sign in' button click.
        """
        # Clear the interface
        self.clear_interface()

        # Функція для валідації введеного значення

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
        lbl_login.place(relx=self.button_config['reg_login_label']['relx'],
                        rely=self.button_config['reg_login_label']['rely'], anchor=tk.W)

        # Create entry field for new login
        self.entry_login = tk.Entry(
            self.root,
            width=int(self.btn_width * 1.5)
        )
        self.entry_login.place(relx=self.button_config['reg_login_entry']['relx'],
                               rely=self.button_config['reg_login_entry']['rely'], anchor=tk.W)

        # Create 'Enter new password' label
        lbl_password = tk.Label(
            self.root,
            text="Enter new password",
            bg=DEFAULT_COLORS['background_color']
        )
        lbl_password.place(relx=self.button_config['reg_password_label']['relx'],
                           rely=self.button_config['reg_password_label']['rely'], anchor=tk.W)

        # Create entry field for new password
        self.entry_password = tk.Entry(
            self.root,
            width=int(self.btn_width * 1.5),
            show="*"
        )
        self.entry_password.place(relx=self.button_config['reg_password_entry']['relx'],
                                  rely=self.button_config['reg_password_entry']['rely'], anchor=tk.W)

        ############################################
        lbl_fname = tk.Label(
            self.root,
            text="Enter your first name",
            bg=DEFAULT_COLORS['background_color']
        )
        lbl_fname.place(relx=self.button_config['reg_firstname_label']['relx'],
                        rely=self.button_config['reg_firstname_label']['rely'], anchor=tk.W)

        self.entry_name = tk.Entry(
            self.root,
            width=int(self.btn_width * 1.5)
        )
        self.entry_name.place(relx=self.button_config['reg_firstname_entry']['relx'],
                              rely=self.button_config['reg_firstname_entry']['rely'], anchor=tk.W)
        ############################################
        ############################################
        lbl_lname = tk.Label(
            self.root,
            text="Enter your second name",
            bg=DEFAULT_COLORS['background_color']
        )
        lbl_lname.place(relx=self.button_config['reg_lastname_label']['relx'],
                        rely=self.button_config['reg_lastname_label']['rely'], anchor=tk.W)

        self.entry_lname = tk.Entry(
            self.root,
            width=int(self.btn_width * 1.5)
        )
        self.entry_lname.place(relx=self.button_config['reg_lastname_entry']['relx'],
                               rely=self.button_config['reg_lastname_entry']['rely'], anchor=tk.W)
        ############################################
        lbl_birth_date = tk.Label(
            self.root,
            text="Enter your date of birth",
            bg=DEFAULT_COLORS['background_color']
        )
        lbl_birth_date.place(relx=self.button_config['reg_birth_date_label']['relx'],
                             rely=self.button_config['reg_birth_date_label']['rely'], anchor=tk.W)

        self.entry_birth_date = tkcalendar.DateEntry(
            self.root,
            width=int(self.btn_width * 1.5),
            date_pattern='yyyy-mm-dd'
        )
        self.entry_birth_date.place(relx=self.button_config['reg_birth_date_entry']['relx'],
                                    rely=self.button_config['reg_birth_date_entry']['rely'], anchor=tk.W)
        ############################################
        lbl_photo = tk.Label(
            self.root,
            text="Enter a link to the photo",
            bg=DEFAULT_COLORS['background_color']
        )
        lbl_photo.place(relx=self.button_config['reg_photo_label']['relx'],
                        rely=self.button_config['reg_photo_label']['rely'], anchor=tk.W)

        self.entry_photo = tk.Entry(
            self.root,
            width=int(self.btn_width * 1.5)
        )
        self.entry_photo.place(relx=self.button_config['reg_photo_entry']['relx'],
                               rely=self.button_config['reg_photo_entry']['rely'], anchor=tk.W)
        ############################################
        ############################################
        lbl_passport = tk.Label(
            self.root,
            text="Enter your passport number",
            bg=DEFAULT_COLORS['background_color']
        )
        lbl_passport.place(relx=self.button_config['reg_passport_number_label']['relx'],
                           rely=self.button_config['reg_passport_number_label']['rely'], anchor=tk.W)

        self.entry_passport = tk.Entry(
            self.root,
            width=int(self.btn_width * 1.5)
        )
        self.entry_passport.place(relx=self.button_config['reg_passport_number_entry']['relx'],
                                  rely=self.button_config['reg_passport_number_entry']['rely'], anchor=tk.W)
        ############################################
        ############################################
        lbl_phone = tk.Label(
            self.root,
            text="Enter your phone number",
            bg=DEFAULT_COLORS['background_color']
        )
        lbl_phone.place(relx=self.button_config['reg_phone_number_label']['relx'],
                        rely=self.button_config['reg_phone_number_entry']['rely'], anchor=tk.W)

        self.entry_phone = tk.Entry(
            self.root,
            width=int(self.btn_width * 1.5)
        )
        self.entry_phone.place(relx=self.button_config['reg_phone_number_entry']['relx'],
                               rely=self.button_config['reg_phone_number_entry']['rely'], anchor=tk.W)
        ############################################
        ############################################
        lbl_licence = tk.Label(
            self.root,
            text="Enter your licence number",
            bg=DEFAULT_COLORS['background_color']
        )
        lbl_licence.place(relx=self.button_config['reg_licence_number_label']['relx'],
                          rely=self.button_config['reg_licence_number_label']['rely'], anchor=tk.W)

        self.entry_licence = tk.Entry(
            self.root,
            width=int(self.btn_width * 1.5)
        )
        self.entry_licence.place(relx=self.button_config['reg_licence_number_entry']['relx'],
                                 rely=self.button_config['reg_licence_number_entry']['rely'], anchor=tk.W)
        ############################################
        ############################################
        lbl_email = tk.Label(
            self.root,
            text="Enter your email number",
            bg=DEFAULT_COLORS['background_color']
        )
        lbl_email.place(relx=self.button_config['reg_email_label']['relx'],
                        rely=self.button_config['reg_email_label']['rely'], anchor=tk.W)

        self.entry_email = tk.Entry(
            self.root,
            width=int(self.btn_width * 1.5)
        )
        self.entry_email.place(relx=self.button_config['reg_email_entry']['relx'],
                               rely=self.button_config['reg_email_entry']['rely'], anchor=tk.W)
        ############################################

        # Create 'Sign Up' button
        btn_create = tk.Button(
            self.root,
            text="Sign Up",
            command=self.check_data,
            width=self.btn_width,
            height=self.btn_height,
            bg=DEFAULT_COLORS['button_color_2']
        )
        btn_create.place(relx=self.button_config['register_button']['relx'],
                         rely=self.button_config['register_button']['rely'], anchor=tk.CENTER)

    def check_data(self):
        self.reset_fields()
        if not self.entry_login.get():
            self.entry_login.config(bg='red')
            return
        if not self.entry_password.get():
            self.entry_password.config(bg='red')
            return
        if not self.entry_name.get():
            self.entry_name.config(bg='red')
            return
        if not self.entry_lname.get():
            self.entry_lname.config(bg='red')
            return
        if not self.entry_photo.get():
            self.entry_photo.config(bg='red')
            return
        # Отримання введених даних з полів
        if self.entry_passport:  # Перевірка, чи поле існує
            passport = self.entry_passport.get()
        else:
            passport = ""  # Значення за замовчуванням, якщо поле пусте або відсутнє
        if self.entry_phone:  # Перевірка, чи поле існує
            phone = self.entry_phone.get()
        else:
            phone = ""  # Значення за замовчуванням, якщо поле пусте або відсутнє
        if self.entry_licence:  # Перевірка, чи поле існує
            license_number = self.entry_licence.get()
        else:
            license_number = ""  # Значення за замовчуванням, якщо поле пусте або відсутнє
        if self.entry_email:  # Перевірка, чи поле існує
            email = self.entry_email.get()
        else:
            email = ""  # Значення за замовчуванням, якщо поле пусте або відсутнє

        # Регулярні вирази для перевірки правильності даних
        passport_pattern = re.compile(r'^.{9}$')
        phone_pattern = re.compile(r'^.{10}$')
        license_pattern = re.compile(r'^.{6}$')
        email_pattern = re.compile(r'^\S+@\S+\.\S+$')

        # Перевірка введених даних
        if not passport_pattern.match(passport):
            # Підсвітити поле паспорта червоним
            self.entry_passport.config(bg='red')
            return

        if not phone_pattern.match(phone):
            # Підсвітити поле телефону червоним
            self.entry_phone.config(bg='red')
            return

        if not license_pattern.match(license_number):
            # Підсвітити поле номеру водійського посвідчення червоним
            self.entry_licence.config(bg='red')
            return

        if not email_pattern.match(email):
            # Підсвітити поле електронної пошти червоним
            self.entry_email.config(bg='red')
            return

        # Якщо всі дані вірні, викликати self.process_signup()
        self.process_signup()

    def reset_fields(self):
        # Скидання підсвічування кольору у всіх полях
        self.entry_password.config(bg='white')
        self.entry_phone.config(bg='white')
        self.entry_licence.config(bg='white')
        self.entry_email.config(bg='white')
        self.entry_login.config(bg='white')
        self.entry_passport.config(bg='white')
        self.entry_name.config(bg='white')
        self.entry_lname.config(bg='white')
        self.entry_photo.config(bg='white')

    def process_login(self):
        """
        Process the login by retrieving login and password information, print them, and display the user interface.
        """
        login = self.entry_login.get()
        password = self.entry_password.get()
        user_logging = LogIn(login, password)
        if user_logging.successful:
            print(f"Logging in with Login: {login}, Password: {password}")
            if user_logging.check_user_role():
                controller = Controller.RenterController(user_logging.user)
                self.show_user_interface(controller)
            else:
                controller = Controller.ManagerController(user_logging.user)
                self.show_worker_interface(controller)
        else:
            print('Logging isn`t successful')
            self.clear_interface()  # Clear the previous interface
            error_login_label = tk.Label(self.root, text="Invalid login. Login error.", font=("Arial", 36))
            error_login_label.place(relx=1, rely=0, anchor=tk.NE, x=400, y=100)

    def show_user_interface(self, controller):
        """
        Display the user interface using the UserInterface class instance in the same window.
        """
        self.clear_interface()  # Clear the previous interface

        # Create an instance of the UserInterface class to display the user interface in the same window
        user_interface = CarHire(self.root, controller)
    def show_worker_interface(self, controller):
        """
        Display the user interface using the UserInterface class instance in the same window.
        """
        self.clear_interface()  # Clear the previous interface

        # Create an instance of the UserInterface class to display the user interface in the same window
        user_interface = UserInterface(self.root, controller)

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
