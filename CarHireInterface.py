import tkinter as tk

from CarDomain import Car


class CarHire:
    def __init__(self, root, controller):
        self.controller = controller
        self.inner_frame = None
        self.filter_frame = None
        self.selected_car_type = None
        self.max_entry = None
        self.min_entry = None
        self.root = root
        self.setup_ui()

    def setup_ui(self):
        """
                Sets up the user interface elements.
                """
        self.create_top_buttons()
        self.create_filter_frame()
        self.create_table_frame()

    def create_top_buttons(self):
        """
                Creates top buttons for the user interface.
                """
        self.create_profile_button()
        self.create_logout_button()

    def create_logout_button(self):
        """
                Creates a logout button.
                """
        logout_button = tk.Button(self.root, text="Log out", command=self.log_out)
        logout_button.place(relx=1, rely=0, anchor=tk.NE, x=-55, y=20)

    def create_profile_button(self):
        """
                Creates a profile button.
                """
        profile_button= tk.Button(self.root, text="My Profile", command=self.open_profile)
        profile_button.place(relx=1, rely=0, anchor=tk.NE, x=-145, y=20)

    def open_profile(self):
        """
                Placeholder method for opening a user profile.
                """
        # Логика открытия профиля
        pass

    def log_out(self):
        """
        Logout function to close the user interface window.
        """
        self.root.destroy()  # Close the window of the user interface

    def create_filter_frame(self):
        """
                Creates a frame for filters and adds filter elements.
                """
        # Create a frame for filters
        self.filter_frame = tk.Frame(self.root, width=800, height=300, bg="white", relief='solid', borderwidth=1)
        self.filter_frame.pack(fill='both', expand=False, padx=(800, 145), pady=(100, 20))

        # Create and place an image on the left side of the filter frame
        img = tk.PhotoImage(file="Emblem_for_car_hire_service.png")
        label_img = tk.Label(self.root, image=img)
        label_img.image = img  # Keep a reference to the image to prevent it from being garbage collected
        label_img.place(relx=0, rely=0, anchor=tk.NW)

        self.create_car_type_filters()
        self.create_filter_button()

    def create_car_type_filters(self):
        """
               Creates car type filters within the filter frame.
               """
        # Logic to create price filters
        filter_label = tk.Label(self.filter_frame, text="Filtering by price", font=("Arial", 12))
        filter_label.grid(row=0, column=5, columnspan=3, pady=(10, 5))

        min_label = tk.Label(self.filter_frame, text="Minimum:")
        min_label.grid(row=1, column=5, padx=5, pady=5)

        self.min_entry = tk.Entry(self.filter_frame)
        self.min_entry.grid(row=1, column=6, padx=5, pady=5)

        max_label = tk.Label(self.filter_frame, text="Maximum:")
        max_label.grid(row=2, column=5, padx=5, pady=5)

        self.max_entry = tk.Entry(self.filter_frame)
        self.max_entry.grid(row=2, column=6, padx=5, pady=5)

        # Create labels and radio buttons for car type filtering
        car_type_label = tk.Label(self.filter_frame, text="Car type", font=("Arial", 12))
        car_type_label.grid(row=0, column=8, columnspan=3, pady=(10, 5))

        self.selected_car_type = tk.StringVar(value="STANDART")  # Variable to store the selected car type

        car_type_options = ["STANDART", "PREMIUM", "ECONOMY", "TRUCK"]
        tk.Radiobutton(self.filter_frame, text="STANDART", variable=self.selected_car_type, value="STANDART").grid(
            row=1,
            column=8,
            columnspan=1,
            padx=5)
        tk.Radiobutton(self.filter_frame, text="PREMIUM", variable=self.selected_car_type, value="PREMIUM").grid(row=2,
                                                                                                                 column=8,
                                                                                                                 columnspan=1,
                                                                                                                 padx=5)
        tk.Radiobutton(self.filter_frame, text="ECONOMY", variable=self.selected_car_type, value="ECONOMY").grid(row=1,
                                                                                                                 column=9,
                                                                                                                 columnspan=1,
                                                                                                                 padx=5)
        tk.Radiobutton(self.filter_frame, text="TRUCK", variable=self.selected_car_type, value="TRUCK").grid(row=2,
                                                                                                             column=9,
                                                                                                             columnspan=1,
                                                                                                             padx=5)

    def create_filter_button(self):
        """
                Creates a filter button within the filter frame.
                """
        filter_button = tk.Button(self.filter_frame, text="Filter", width=15, height=3, command=self.check_data, font=("Arial", 12))
        filter_button.grid(row=1, column=0, columnspan=1, rowspan=3, padx=20, pady=10)

    def apply_filter(self):
        """
                Applies filters to the table based on user inputs.
                """
        min_value = self.min_entry.get()
        max_value = self.max_entry.get()
        selected_type = self.selected_car_type.get()  # Get the selected car type
        for widget in self.inner_frame.winfo_children():
            widget.destroy()
        cars = self.controller.get_filtered_cars((float(min_value), float(max_value)), selected_type)
        car_num = len(cars)
        rows = int(car_num / 3)
        last_row = car_num % 3
        self.car_table(rows, last_row, cars)

    def check_data(self):
        """
                Checks and validates the user input data for filtering.
                """
        self.reset_fields()  # Спочатку скидаємо попереднє підсвічування

        if not self.min_entry.get().isdigit():
            self.min_entry.config(bg='red')

        if not self.max_entry.get().isdigit():
            self.max_entry.config(bg='red')

        if not self.min_entry.get().isdigit() or not self.max_entry.get().isdigit():
            return  # Якщо хоча б одне поле не є числом, припиняємо перевірку

        if int(self.min_entry.get()) > int(self.max_entry.get()):
            self.min_entry.config(bg='red')
            self.max_entry.config(bg='red')
            return
        self.apply_filter()

    def reset_fields(self):
        """
                Resets the color highlighting of input fields.
                """
        # Скидання підсвічування кольору у всіх полях
        self.min_entry.config(bg='white')
        self.max_entry.config(bg='white')

    def create_table_frame(self):
        """
                Creates a scrollable frame for displaying table content.
                """
        # Logic to create the table
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill='both', expand=True, padx=30, pady=(20, 40))

        canvas = tk.Canvas(table_frame)
        canvas.pack(side=tk.LEFT, fill='both', expand=True)

        scrollbar = tk.Scrollbar(table_frame, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        self.inner_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        cars = self.controller.get_available_cars()
        car_num = len(cars)
        rows = int(car_num / 3)
        last_row = car_num % 3
        self.car_table(rows, last_row, cars)

    def rent_apply(self, car: Car):
        """
                Creates a section for entering rental days and renting a car.
                """
        for widget in self.root.winfo_children():
            widget.destroy()
        rental_frame = tk.Frame(self.root, width=400, height=200, bg="white", relief='solid', borderwidth=1)
        rental_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        days_label = tk.Label(rental_frame, text="Введіть кількість днів для оренди", font=("Arial", 12))
        days_label.grid(row=0, column=0, columnspan=2, pady=(10, 5))

        days_entry = tk.Entry(rental_frame)
        days_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        rent_button = tk.Button(rental_frame, text="Орендувати", width=15, height=2,
                                command=lambda: self.rent_car(days_entry.get(), car), font=("Arial", 12))
        rent_button.grid(row=2, column=0, columnspan=2, pady=10)

    def rent_car(self, days, car: Car):
        """
        Rents a car for the specified number of days.

        Parameters:
            days (str): Number of days for car rental.
            :param car:
        """
        # Logic to rent a car for the specified number of days
        rent = self.controller.rent_car(car, int(days))

        # Hide widgets instead of destroying them
        for widget in self.root.winfo_children():
            widget.destroy()

        # Display success message and logout button
        thanks_label = tk.Label(self.root, text="Thank you for renting.", font=("Arial", 16))
        thanks_label.pack(pady=50)

        logout_button = tk.Button(self.root, text="Log out", command=self.root.destroy)
        logout_button.pack()

    def car_table(self, rows, last_row, cars):
        """
                Generates and populates the car table within the scrollable frame.

                Parameters:
                    rows (int): Number of rows in the table.
                    last_row (int): Number of cells in the last row.
                    cars (list[Car]): List of Car objects to display.
                """
        columns = 3
        cell_width = (self.root.winfo_screenwidth() - 200) // columns  # Width of each cell considering padding
        id_counter = 0
        for row in range(rows):  # Create multiple rows
            for col in range(columns):  # Create cells in each row
                cell_frame = tk.Frame(self.inner_frame, width=cell_width, height=300, relief='solid', borderwidth=1)
                cell_frame.pack_propagate(False)
                cell_frame.grid(row=row, column=col, padx=5, pady=5)  # Position cells within the row

                # Inside the loops where you create cells
                label_img = tk.Label(cell_frame)
                label_img.grid(row=0, column=0, rowspan=6)  # Займає 4 рядки для зображення

                # Load and assign image to the label
                img = tk.PhotoImage(file="funny-car-photo-conceptual-art.png")
                img = img.subsample(3, 3)
                label_img.config(image=img)
                label_img.image = img  # Keep a reference to prevent garbage collection
                price = cars[id_counter].rentPrice
                model = cars[id_counter].carModel
                car_type = cars[id_counter].carType
                deposit = self.controller.calculate_deposit(price)
                label_temp = tk.Label(cell_frame, text=f"                      ")
                label_temp.grid(row=0, column=3)
                label_temp2 = tk.Label(cell_frame, text=f"                                                    ")
                label_temp2.grid(row=0, column=2)
                label_price = tk.Label(cell_frame, text=f"Price: ${price}", font=("Arial", 12))
                label_price.grid(row=1, column=1, columnspan=3)
                label_model = tk.Label(cell_frame, text=f"Model: {model}", font=("Arial", 12))
                label_model.grid(row=2, column=2, columnspan=3)

                label_type = tk.Label(cell_frame, text=f"Type: {car_type}", font=("Arial", 12))
                label_type.grid(row=3, column=2, columnspan=3)

                label_deposit = tk.Label(cell_frame, text=f"Deposit: {deposit}", font=("Arial", 12))
                label_deposit.grid(row=4, column=2, columnspan=3)
                filter_button = tk.Button(
                    cell_frame,
                    text="Rent",
                    width=15,
                    height=3,
                    command=lambda car=cars[id_counter]: self.rent_apply(car),
                    font=("Arial", 12)
                )
                filter_button.grid(row=5, column=2, columnspan=3, rowspan=3, pady=(0, 10))
                id_counter = id_counter + 1

        if last_row > 0:
            for col in range(last_row):
                cell_frame = tk.Frame(self.inner_frame, width=cell_width, height=300, relief='solid', borderwidth=1)
                cell_frame.pack_propagate(False)
                cell_frame.grid(row=rows + 1, column=col, padx=5, pady=5)  # Position cells within the row
                # Inside the loops where you create cells
                label_img = tk.Label(cell_frame)
                label_img.grid(row=0, column=0, rowspan=6)  # Займає 4 рядки для зображення

                # Load and assign image to the label
                img = tk.PhotoImage(file="funny-car-photo-conceptual-art.png")
                img = img.subsample(3, 3)
                label_img.config(image=img)
                label_img.image = img  # Keep a reference to prevent garbage collection
                price = cars[id_counter].rentPrice
                model = cars[id_counter].carModel
                car_type = cars[id_counter].carType
                deposit = self.controller.calculate_deposit(price)
                label_temp = tk.Label(cell_frame, text=f"                      ")
                label_temp.grid(row=0, column=3)
                label_temp2 = tk.Label(cell_frame, text=f"                                                    ")
                label_temp2.grid(row=0, column=2)
                label_price = tk.Label(cell_frame, text=f"Price: ${price}", font=("Arial", 12))
                label_price.grid(row=1, column=1, columnspan=3)
                label_model = tk.Label(cell_frame, text=f"Model: {model}", font=("Arial", 12))
                label_model.grid(row=2, column=2, columnspan=3)

                label_type = tk.Label(cell_frame, text=f"Type: {car_type}", font=("Arial", 12))
                label_type.grid(row=3, column=2, columnspan=3)

                label_deposit = tk.Label(cell_frame, text=f"Deposit: {deposit}", font=("Arial", 12))
                label_deposit.grid(row=4, column=2, columnspan=3)
                filter_button = tk.Button(cell_frame, text="Rent", width=15, height=3,
                                          command=self.rent_apply, font=("Arial", 12))
                filter_button.grid(row=5, column=2, columnspan=3, rowspan=3, pady=(0, 10))
                id_counter = id_counter + 1

