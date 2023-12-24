import tkinter as tk


class EmployeeInterface:
    # Initializing attributes and setting up the interface
    def __init__(self, root, controller):
        self.frame_drivers = None
        self.frame_cars = None
        self.controller = controller
        self.optionsRentability_vars = None
        self.selected_rentability = None
        self.optionsType = None
        self.optionsRental = None
        self.root = root
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.setup_ui()
        self.selected_rental_statuses = []
        self.selected_types = []
        self.optionsRental_vars = []
        self.optionsType_vars = []

    def setup_ui(self):
        """
                Sets up the user interface elements.
                """
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")
        self.create_scrollable_frame()
        self.create_logout_button()
        self.create_three_frames()

    def create_scrollable_frame(self):
        """
                Creates a scrollable frame for content.
                """
        canvas = tk.Canvas(self.root)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(self.root, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.configure(yscrollcommand=scrollbar.set)

        self.inner_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.add_content_to_frame()

        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    def add_content_to_frame(self):
        """
                Adds content to the scrollable frame.
                """
        # Додайте сюди вміст, який ви плануєте розмістити в прокручуваному вікні
        pass

    def create_logout_button(self):
        """
                Creates a logout button.
                """
        logout_button = tk.Button(self.root, text="Log out", command=self.log_out)
        logout_button.place(relx=1, rely=0, anchor=tk.NE, x=-25, y=10)

    def log_out(self):
        """
               Logs out and destroys the interface.
               """
        self.root.destroy()

    def create_three_frames(self):
        """
               Creates three frames for different functionalities.
               """
        frame_padx_left = 10
        frame_padx_right = 30
        frame_pady_top = 300
        frame_pady_bottom = 20
        frame_spacing = 10  # Проміжок між фреймами

        frame_width = (
                                  self.screen_width - 2 * frame_padx_left - 2 * frame_padx_right - 2 * frame_spacing - frame_pady_bottom) // 3 - 50
        frame_height = self.screen_height - frame_pady_top

        self.fill_drivers_top_frame()
        self.fill_cars_top_frame()
        frame_contracts_top = tk.Button(self.inner_frame, text="Solve problems", command=self.solve_problems,
                                        font=("Arial", 12), width=40, height=10)

        frame_contracts_top.grid(row=0, column=2, padx=(frame_padx_left, frame_padx_right),
                                 pady=(50, 0))
        users = self.controller.get_users()
        cars = self.controller.get_cars()
        expired_rents = self.controller.get_expired_rents()
        label_drivers = tk.Label(self.inner_frame, text="Drivers", font=("Arial", 12))
        label_drivers.grid(row=1, column=0, padx=(frame_padx_left, frame_padx_right), pady=(20, frame_pady_bottom // 2))

        self.frame_drivers = tk.Frame(self.inner_frame, width=frame_width, height=frame_height, bg="white")
        self.frame_drivers.grid(row=2, column=0, padx=(frame_padx_left, frame_padx_right), pady=(10, frame_pady_bottom))
        self.drivers_table(users)

        label_cars = tk.Label(self.inner_frame, text="Cars", font=("Arial", 12))
        label_cars.grid(row=1, column=1, padx=(frame_padx_left, frame_padx_right), pady=(20, frame_pady_bottom // 2))

        self.frame_cars = tk.Frame(self.inner_frame, width=frame_width, height=frame_height, bg="white")
        self.frame_cars.grid(row=2, column=1, padx=(frame_padx_left, frame_padx_right), pady=(10, frame_pady_bottom))
        self.cars_table(cars)

        label_contracts = tk.Label(self.inner_frame, text="Contracts", font=("Arial", 12))
        label_contracts.grid(row=1, column=2, padx=(frame_padx_left, frame_padx_right),
                             pady=(20, frame_pady_bottom // 2))

        frame_contracts = tk.Frame(self.inner_frame, width=frame_width + 100, height=frame_height, bg="white")
        frame_contracts.grid(row=2, column=2, padx=(frame_padx_left, frame_padx_right), pady=(10, frame_pady_bottom))
        self.contracts_table(frame_contracts, expired_rents)

        # Додано сітки грід в кожний фрейм
        self.frame_drivers.grid_propagate(False)
        self.frame_cars.grid_propagate(False)
        frame_contracts.grid_propagate(False)

    def solve_problems(self):
        """
                Placeholder method for solving problems.
                """
        pass

    def fill_drivers_top_frame(self):
        """
                Fills the top frame related to drivers with filter options.
                """
        frame_padx_left = 10
        frame_padx_right = 30
        frame_pady_bottom = 20
        frame_spacing = 10  # Проміжок між фреймами
        frame_width = (
                                  self.screen_width - 2 * frame_padx_left - 2 * frame_padx_right - 2 * frame_spacing - frame_pady_bottom) // 3 - 50
        frame_drivers_top = tk.Frame(self.inner_frame, width=frame_width, height=200, bg="white")
        frame_drivers_top.grid(row=0, column=0, sticky="nsew", padx=(frame_padx_left, frame_padx_right),
                               pady=(50, 0))
        filter_button_drivers = tk.Button(frame_drivers_top, text="Filter", command=self.filter_drivers)
        filter_button_drivers.grid(row=0, column=0, rowspan=5, columnspan=3, sticky="nsew", padx=5, pady=5)
        labeltemp = tk.Label(frame_drivers_top, text="     ", font=("Arial", 10), bg="white", fg="black")
        labeltemp.grid(row=0, column=3, padx=5, pady=5)

        label_rentability = tk.Label(frame_drivers_top, text="Rentability:", font=("Arial", 10), bg="white", fg="black")
        label_rentability.grid(row=0, column=4, padx=5, pady=5)

        options = ["Yes", "No"]
        self.optionsRentability_vars = []

        for i, option in enumerate(options, start=2):
            varRentability = tk.IntVar(value=0)
            checkbox = tk.Checkbutton(frame_drivers_top, text=option, font=("Arial", 10), bg="white", fg="black",
                                      variable=varRentability)
            checkbox.grid(row=i, column=4, padx=5, pady=5, sticky="w")
            self.optionsRentability_vars.append(varRentability)

    def fill_cars_top_frame(self):
        """
                Fills the top frame related to cars with filter options.
                """
        frame_padx_left = 10
        frame_padx_right = 30
        frame_pady_top = 300
        frame_pady_bottom = 20
        frame_spacing = 10  # Проміжок між фреймами
        frame_width = (
                              self.screen_width - 2 * frame_padx_left - 2 * frame_padx_right - 2 * frame_spacing - frame_pady_bottom) // 3 - 50
        frame_height = self.screen_height - frame_pady_top
        frame_cars_top = tk.Frame(self.inner_frame, width=frame_width, height=200, bg="white")
        frame_cars_top.grid(row=0, column=1, sticky="nsew", padx=(frame_padx_left, frame_padx_right),
                            pady=(50, frame_pady_bottom // 2))

        filter_button_cars = tk.Button(frame_cars_top, text="Filter", command=self.filter_cars)
        filter_button_cars.grid(row=0, column=0, rowspan=6, sticky="nsew", padx=5, pady=5)

        label_status = tk.Label(frame_cars_top, text="Rental status:", font=("Arial", 10), bg="white", fg="black")
        label_status.grid(row=0, column=2, padx=5, pady=5)
        labeltemp = tk.Label(frame_cars_top, text="     ", font=("Arial", 10), bg="white", fg="black")
        labeltemp.grid(row=0, column=1, padx=5, pady=5)

        self.optionsRental = ["IN_RENT", "AVAILABLE", "SERVICED"]
        self.optionsRental_vars = []  # Додано ініціалізацію змінної self.optionsRental_vars

        for i, option in enumerate(self.optionsRental, start=1):
            var1 = tk.IntVar(value=0)
            checkbox = tk.Checkbutton(frame_cars_top, text=option, font=("Arial", 10), bg="white", fg="black",
                                      variable=var1)
            checkbox.grid(row=i, column=2, padx=5, pady=5, sticky="w")
            self.optionsRental_vars.append(var1)  # Додано до списку self.optionsRental_vars

        label_type = tk.Label(frame_cars_top, text="Type:", font=("Arial", 10), bg="white", fg="black")
        label_type.grid(row=0, column=4, padx=5, pady=5)
        labeltemp = tk.Label(frame_cars_top, text="     ", font=("Arial", 10), bg="white", fg="black")
        labeltemp.grid(row=0, column=3, padx=5, pady=5)

        self.optionsType = ["STANDART", "PREMIUM", "ECONOMY", "TRUCK"]
        self.optionsType_vars = []  # Додано ініціалізацію змінної self.optionsType_vars

        for i, option in enumerate(self.optionsType, start=1):
            var2 = tk.IntVar(value=0)
            checkbox = tk.Checkbutton(frame_cars_top, text=option, font=("Arial", 10), bg="white", fg="black",
                                      variable=var2)
            checkbox.grid(row=i, column=4, padx=5, pady=5, sticky="w")
            self.optionsType_vars.append(var2)

    def drivers_table(self, users):
        """
                Creates a table to display driver information.

                Parameters:
                    users (list[User]): List of User objects representing drivers.
                """
        labels_drivers = ["First name", "Last name", "License", "Rentability"]
        # Очистка фрейму перед додаванням нових елементів
        for widget in self.frame_drivers.winfo_children():
            widget.destroy()

        for i, text in enumerate(labels_drivers):
            label = tk.Label(self.frame_drivers, text=text, font=("Arial", 9), bg="white")
            label.grid(row=0, column=i, padx=5, pady=5, sticky="w")

        for idx, user in enumerate(users, start=1):
            user_info = [user.baseInfo.firstName, user.baseInfo.lastName, user.canRent]
            for i, info in enumerate(user_info):
                label = tk.Label(self.frame_drivers, text=info, font=("Arial", 9), bg="white")
                label.grid(row=idx, column=i, padx=5, pady=5, sticky="w")

    def cars_table(self, cars):
        """
                Creates a table to display car information.

                Parameters:
                    cars (list[Car]): List of Car objects.
                """

        labels_cars = ["Number", "Model", "Price", "Rental status", "Type"]
        # Очистка фрейму перед додаванням нових елементів
        for widget in self.frame_cars.winfo_children():
            widget.destroy()
        for i, text in enumerate(labels_cars):
            label = tk.Label(self.frame_cars, text=text, font=("Arial", 9), bg="white")
            label.grid(row=0, column=i, padx=5, pady=5, sticky="w")

        for idx, car in enumerate(cars, start=1):
            car_info = [car.carNumber, car.carModel, car.rentPrice, car.rentStatus, car.carType]
            for i, info in enumerate(car_info):
                label = tk.Label(self.frame_cars, text=info, font=("Arial", 9), bg="white")
                label.grid(row=idx, column=i, padx=5, pady=5, sticky="w")

    def contracts_table(self, frame, expired_rents):
        """
                Creates a table to display contract information.

                Parameters:
                    frame (tk.Frame): Frame to place the contract table.
                    expired_rents (list[Rent]): List of expired Rent objects.
                """

        labels_contracts = ["First name", "Last name", "Car number", "Rental status", "Rental expiration date"]

        for i, text in enumerate(labels_contracts):
            label = tk.Label(frame, text=text, font=("Arial", 9), bg="white")
            label.grid(row=0, column=i, padx=5, pady=5, sticky="w")

        for idx, rent in enumerate(expired_rents, start=1):
            rent_info = [rent.firstName, rent.lastName, rent.carNumber, rent.isRentFinished, rent.rentExpirationDate]
            for i, info in enumerate(rent_info):
                label = tk.Label(frame, text=info, font=("Arial", 9), bg="white")
                label.grid(row=idx, column=i, padx=5, pady=5, sticky="w")

    def filter_drivers(self):
        """
                Filters drivers based on selected criteria.
                """
        self.selected_rentability = []

        for i, varRentability in enumerate(self.optionsRentability_vars):
            if varRentability.get() == 1:
                self.selected_rentability.append(True if i == 0 else False)

        self.apply_drivers_filter()

    def apply_drivers_filter(self):
        """
                Applies filters to the drivers' table.
                """
        users = self.controller.get_filtered_users(self.selected_rentability)
        self.drivers_table(users)

    def filter_cars(self):
        """
                Filters cars based on selected criteria.
                """

        self.selected_rental_statuses.clear()
        self.selected_types.clear()

        for i, var1 in enumerate(self.optionsRental_vars):
            if var1.get() == 1:
                self.selected_rental_statuses.append(self.optionsRental[i])

        for i, var2 in enumerate(self.optionsType_vars):
            if var2.get() == 1:
                self.selected_types.append(self.optionsType[i])

        self.apply_cars_filter()

    def apply_cars_filter(self):
        """
                Applies filters to the cars' table.
                """
        cars = self.controller.get_filtered_cars(self.selected_rental_statuses, self.selected_types)
        self.cars_table(cars)

