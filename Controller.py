from datetime import datetime, timedelta
from CarDomain import Car
from Users import Renter, CompanyWorker
from typing import Dict


class Rent:
    def __init__(self, rent_id: int | None = None, user_id: int | None = None, car_id: int | None = None,
                 price: float | None = None, discount: int | None = None, deposit: float | None = None,
                 start_time: datetime | None = datetime.now().date(), end_time: datetime | None = datetime.now().date(),
                 agreement: str | None = None, agreement_description: str | None = None,
                 isRentFinished: bool | None = False) -> None:
        """
        Initializes the Rent object with optional parameters.

        Args:
            rent_id (int | None): Unique identifier for the rent.
            user_id (int | None): User ID associated with the rent.
            car_id (int | None): Car ID associated with the rent.
            car_price (float | None): Rental price per day for the car.
            discount (int | None): Discount applied to the rental price.
            deposit (float | None): Deposit amount for the rent.
            days_for_rent (int | None): Number of days the car is rented.
            agreement (str | None): Agreement details for the rent.
            agreement_description (str | None): Description of the rent agreement.

        Note:
            If `rent_id` is not provided, it generates a new agreement and description.
            Otherwise, it uses the provided `agreement` and `agreement_description`.
        """
        self.rent_id: int | None = rent_id
        self.user_id: int | None = user_id
        self.car_id: int | None = car_id
        self.price: float | None = price
        self.discount: int | None = discount
        self.deposit: float | None = deposit
        self.start_time: datetime = start_time
        self.end_time: datetime = end_time
        self.agreement: str | None = agreement
        self.agreement_description: str | None = agreement_description
        self.isRentFinished: bool = isRentFinished

    def generate_agreement(self) -> str:
        """
        Generates a new agreement for the rent.

        Returns:
            str: Agreement details.
        """
        # Placeholder for actual implementation
        pass

    def generate_agreement_description(self) -> str:
        """
        Generates a description for the rent agreement.

        Returns:
            str: Agreement description.
        """
        # Placeholder for actual implementation
        pass

    def upload_to_database_new(self) -> None:
        """
        Uploads new rent details to the database.
        """
        # Placeholder for actual implementation
        id = None  # get new id
        if id is not None:
            self.id = id
        pass

    def upload_to_database_existing(self) -> None:
        """
        Uploads existing rent details to the database.
        """
        # Placeholder for actual implementation
        pass

    def load_from_database(self) -> None:
        """
        Loads rent details from the database.
        """
        if self.rent_id is not None:
            # Placeholder for actual implementation
            pass

    def set_rent_finished(self, set_finished: bool = True) -> None:
        """
        Marks the rent as set_finished and updates the database.

        Args:
            set_finished (bool): Indicates whether the rent is finished or not.
        """
        if self.rent_id is not None:
            self.isRentFinished = set_finished
            # Placeholder for actual implementation - update the Rent table in the database


class RenterController:
    def __init__(self, renter: Renter) -> None:
        """
        Initializes the RenterController object.

        Args:
            renter (Renter): Renter from LogIn.user or Registration.user
        """
        self.renter: Renter = renter

    def calculate_discount(self) -> int:
        """
        Calculates the discount based on the time a user has spent in the system.

        Returns:
            int: Discount percentage.
        """
        time_in_system = self.renter.count_time_in_system()
        if time_in_system >= 365:
            return 10
        elif time_in_system >= 180:
            return 5
        elif time_in_system >= 90:
            return 3
        elif time_in_system >= 30:
            return 1
        else:
            return 0

    def calculate_deposit(self) -> float:
        """
        Calculates the deposit amount based on user information.

        Returns:
            float: Deposit amount.
        """
        # Placeholder for actual implementation
        pass

    def get_available_cars(self) -> list[Car]:
        """
        Retrieves available cars from the Car table in the database.

        Returns:
            list[Car]: List of available cars.
        """
        # Placeholder for actual implementation
        pass

    def rent_car(self, car: Car, days_for_rent: int) -> None:
        """
        Rents a car for a specified number of days and updates the database.

        Args:
            car (Car): Car object to be rented.
            days_for_rent (int): Number of days for the rent.
        """
        rent = Rent(user_id=self.renter.id, car_id=car.carId, price=car.rentPrice * days_for_rent,
                    discount=self.calculate_discount(), deposit=self.calculate_deposit(), start_time=datetime.now().date(),
                    end_time=datetime.now().date() + timedelta(days=days_for_rent))
        rent.generate_agreement()
        rent.generate_agreement_description()
        rent.upload_to_database_new()
        car.set_rent_status('IN_RENT')
        self.renter.set_rent_ability(False)


class ManagerController:
    def __init__(self, manager: CompanyWorker) -> None:
        """
        Initializes the ManagerController object.

        Args:
            manager (CompanyWorker): Manager object from LogIn.user.
        """
        self.manager: CompanyWorker = manager

    def end_rent(self, rent: Rent) -> None:
        """
        Ends the specified rent and updates the database.

        Args:
            rent (Rent): Rent to be ended
        """
        rent.set_rent_finished()
        rent.upload_to_database_existing()

    def change_user_info(self, user: Renter, new_info: Dict[str, str]) -> None:
        """
        Changes user information and updates the database.

        Args:
            user (User): User object.
            new_info (Dict[str, str]): Dictionary containing new user information.
        """
        try:
            if not user.change_base_info(new_info):
                raise Exception
        except Exception as e:
            print('Changing user info failed')

    def get_users(self) -> list[Renter]:
        """
        Retrieves a list of users from the User table in the database.

        Returns:
            list[Renter]: List of users.
        """
        # Placeholder for actual implementation
        pass

    def get_cars(self) -> list[Car]:
        """
        Retrieves a list of cars from the Car table in the database.

        Returns:
            list[Car]: List of cars.
        """
        # Placeholder for actual implementation
        pass

    def get_rented_cars(self) -> list[Car]:
        """
        Retrieves a list of rented cars from the Rent table in the database.

        Returns:
            list[Car]: List of rented cars.
        """
        # Placeholder for actual implementation
        pass

    def get_expired_rents(self) -> list[Rent]:
        """
        Retrieves a list of expired rents from the Rent table in the database.

        Returns:
            list[Rent]: List of expired rents.
        """
        # Placeholder for actual implementation
        pass
