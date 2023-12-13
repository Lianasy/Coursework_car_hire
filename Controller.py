from datetime import datetime
from CarDomain import Car
from Users import Renter
from typing import Dict


class Rent:
    def __init__(self, rent_id: int | None = None, user_id: int | None = None, car_id: int | None = None,
                 car_price: float | None = None, discount: int | None = None, deposit: float | None = None,
                 days_for_rent: int | None = None, agreement: str | None = None,
                 agreement_description: str | None = None) -> None:
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
        self.price: float | None = car_price * days_for_rent
        self.discount: int | None = discount
        self.deposit: float | None = deposit
        self.start_time: datetime = datetime.now().date()
        self.end_time: datetime = self.start_time + days_for_rent
        if rent_id is None:
            self.agreement: str = self.generate_agreement()
            self.agreement_description: str = self.generate_agreement_description()
        else:
            self.agreement: str = agreement
            self.agreement_description: str = agreement_description
        self.isRentFinished: bool = False

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

    def upload_rent(self) -> None:
        """
        Uploads rent details to the database.
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
    def __init__(self) -> None:
        """
        Initializes the RenterController object.

        """
        self.driver_id: int | None = id


    def calculate_discount(self, time_in_system: datetime) -> int:
        """
        Calculates the discount based on the time a user has spent in the system.

        Args:
            time_in_system (datetime): Time in the system (duration).

        Returns:
            int: Discount percentage.
        """
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

    def calculate_deposit(self, driver: Renter) -> float:
        """
        Calculates the deposit amount based on user information.

        Args:
            driver (Renter): User (Renter) object.

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

    def rent_car(self, user: Renter, car: Car, days_for_rent: int) -> None:
        """
        Rents a car for a specified number of days and updates the database.

        Args:
            user (Renter): User (Renter) object.
            car (Car): Car object to be rented.
            days_for_rent (int): Number of days for the rent.
        """
        rent = Rent(user_id=user.id, car_id=car.id, car_price=car.rentPrice,
                    discount=self.calculate_discount(user.count_time_in_system()),
                    deposit=self.calculate_deposit(user), days_for_rent=days_for_rent)
        rent.upload_rent()
        car.setRentStatus('IN_RENT')
        user.set_rent_ability(False)


class ManagerController:
    def __init__(self, id: int) -> None:
        """
        Initializes the ManagerController object.

        Args:
            id (int): User ID associated with the controller.
        """
        self.manager_id: int = id

    def end_rent(self, rent_id: int) -> None:
        """
        Ends the specified rent and updates the database.

        Args:
            rent_id (int): Rent ID to be ended.
        """
        rent = Rent(rent_id)
        rent.set_rent_finished()

    def change_user_info(self, user: Renter, new_info: Dict[str, str]) -> None:
        """
        Changes user information and updates the database.

        Args:
            user (User): User object.
            new_info (Dict[str, str]): Dictionary containing new user information.
        """
        user.change_base_info(new_info)

    def get_users(self) -> list:
        """
        Retrieves a list of users from the User table in the database.

        Returns:
            list: List of users.
        """
        # Placeholder for actual implementation
        pass

    def get_cars(self) -> list:
        """
        Retrieves a list of cars from the Car table in the database.

        Returns:
            list: List of cars.
        """
        # Placeholder for actual implementation
        pass

    def get_rented_cars(self) -> list:
        """
        Retrieves a list of rented cars from the Rent table in the database.

        Returns:
            list: List of rented cars.
        """
        # Placeholder for actual implementation
        pass

    def get_expired_rents(self) -> list:
        """
        Retrieves a list of expired rents from the Rent table in the database.

        Returns:
            list: List of expired rents.
        """
        # Placeholder for actual implementation
        pass
