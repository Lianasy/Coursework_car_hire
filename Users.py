from datetime import datetime
from typing import Dict


class BaseInfo:
    def __init__(self, id: int, firstName: str = None, lastName: str = None, birthDate: datetime = None) -> None:
        """
        Initializes the BaseInfo object with optional parameters.

        Args:
            id (int): The user ID.
            firstName (str): First name of the user.
            lastName (str): Last name of the user.
            birthDate (datetime): Birthdate of the user.

        Note:
            If `firstName`, `lastName`, and `birthDate` aren't provided, they will be loaded from the database automatically.
            Otherwise, they will be added to the database automatically.
        """
        self.id: int = id
        self.firstName: str | None = firstName
        self.lastName: str | None = lastName
        self.birthDate: datetime | None = birthDate
        if id is None:
            self.load_base_info()
        else:
            self.upload_base_info()

    def upload_base_info(self) -> None:
        """
        Uploads user's base information to the database.
        """
        # Placeholder for actual implementation

    def load_base_info(self) -> None:
        """
        Loads user's base information from the database.
        """
        if self.id is not None:
            # Placeholder for actual implementation
            pass


class Credential:
    def __init__(self, login: str, password: str) -> None:
        """
        Initializes the Credential object with login and password.

        Args:
            login (str): User's login.
            password (str): Password which user writes when logging in.
        """
        self.login: str = login
        self.password_to_validate: str = password

    def get_id(self) -> int | None:
        """
        Gets the user ID if the password is valid.

        Returns:
            int | None: User ID or None if the password is invalid.
        """
        if self.__to_valid_password():
            # Placeholder for actual implementation
            pass
        else:
            return None

    def __get_password(self) -> str:
        """
        Retrieves the password from the database based on the login.

        Returns:
            str: User's password.
        """
        # Placeholder for actual implementation
        pass

    def __to_valid_password(self) -> bool:
        """
        Validates if the provided password matches the stored password.

        Returns:
            bool: True if the password is valid, False otherwise.
        """
        return self.__get_password() == self.password_to_validate

    def update_login(self, new_login: str) -> None:
        """
        Updates the user's login and reflects the change in the database.

        Args:
            new_login (str): New login for the user.
        """
        old_login: str = self.login
        self.login = new_login
        # Placeholder for actual implementation

    def update_password(self, new_password: str) -> None:
        """
        Updates the user's password and reflects the change in the database.

        Args:
            new_password (str): New password for the user.
        """
        # Placeholder for actual implementation


class PrivateInfo:
    def __init__(self, id: int = None, privateInfo: Dict[str, str | None] = None) -> None:
        """
        Initializes the PrivateInfo object with a user ID.

        Args:
            id (int): User ID. If not provided, upload given privateInfo to the database by method `upload_private_info`
            and get id for new user
        """
        self.id: int = id
        if id is None:
            self.id = self.upload_private_info(privateInfo)

    def get_private_info(self) -> Dict[str, str | None]:
        """
        Retrieves private information of the user from the database.

        Returns:
            Dict[str, str | None]: Dictionary containing private information.
        """
        info: Dict[str, str | None] = None
        return info.copy() if info else {}

    def upload_private_info(self, args: Dict[str, str | None]) -> int:
        """
        Uploads private information of the user to the database.
        if self.id isn't specified, gets it from the database

        Args:
            args (Dict[str, str | None]): Dictionary containing private information.

        Returns:
            int: User id
        """
        # Placeholder for actual implementation
        # if self.id is None (new user), get a new id
        return self.id


class User:
    def __init__(self, id: int = None) -> None:
        """
        Initializes the User object with optional parameters.

        Args:
            id (int | None): User ID.
        """
        self.id: int | None = id
        self.baseInfo: BaseInfo | None = None
        self.load_base_info()
        self.privateInfo: PrivateInfo | None = None
        self.load_private_info()
        self.creds: Credential | None = None

    def load_private_info(self) -> None:
        """
        Loads user's private information from the database.
        """
        if self.id is not None:
            self.privateInfo = PrivateInfo(self.id)
        else:
            self.privateInfo = None

    def load_base_info(self) -> None:
        """
        Loads user's base information from the database.
        """
        if self.id is not None:
            self.baseInfo = BaseInfo(self.id)
        else:
            self.baseInfo = None

    def change_base_info(self, new_info: Dict[str, str | None]) -> None:
        """
        Changes user's base information and updates it in the database.

        Args:
            new_info (Dict[str, str | None]): Dictionary containing new base information
                                               in format {'firstName': str, 'lastName': str, 'birthDate': datetime}.
        """
        # Placeholder for actual implementation
        self.baseInfo.firstName = new_info['firstName']
        self.baseInfo.lastName = new_info['lastName']
        self.baseInfo.birthDate = new_info['birthDate']
        self.baseInfo.upload_base_info()

    def change_private_info(self, new_info: Dict[str, str | None]) -> None:
        """
        Changes user's private information and updates it in the database.

        Args:
            new_info (Dict[str, str | None]): Dictionary containing new private information.
        """
        self.privateInfo.upload_private_info(new_info)

    def change_credentials(self, new_info: Dict[str, str]) -> None:
        """
        Changes user's credentials (login and password) and updates them in the database.

        Args:
            new_info (Dict[str, str]): Dictionary containing new credentials.
        """
        self.creds.update_password(new_info['password'])
        self.creds.update_login(new_info['login'])


class Renter(User):
    def __init__(self, id: int = None) -> None:
        """
        Initializes the Renter object with additional attributes.

        Args:
            id (int): Renter id
        """
        super().__init__(id)
        self.registrationDate: datetime | None = None
        self.driverLicenseDate: datetime | None = None
        self.canRent: bool = True

    def load_from_database(self) -> None:
        """
            Loads renter's information from the database.
        """
        if self.id is not None:
            # Load from database: registrationDate, driverLicenseDate, canRent
            pass

    def register(self, args: Dict[str, str]) -> None:
        """
        Registers a new renter and inserts their information into the database.

        Args:
            args (Dict[str, str]): Dictionary containing information for registration.
        """
        # Placeholder for actual implementation
        # Insert entered data into tables, don't forget to check login for uniqueness
        # self.privateInfo = PrivateInfo(privateInfo) from args
        self.id = self.privateInfo.id
        # self.baseInfo = BaseInfo(self.id, firstName, lastName, birthDate) from args
        self.registrationDate = datetime.now().date()
        # self.driverLicenceDate take from args

    def count_driver_experience(self) -> datetime:
        """
        Calculates the driver experience based on the current date and driver's license date.

        Returns:
            datetime: Driver experience duration.
        """
        return datetime.now().date() - self.driverLicenseDate

    def count_time_in_system(self) -> datetime:
        """
        Calculates the time spent in the system based on the current date and registration date.

        Returns:
            datetime: Time in the system duration.
        """
        return datetime.now().date() - self.registrationDate

    def get_agreements(self) -> None:
        """
        Retrieves agreements from the Agreement document based on the user ID.
        """
        pass

    def set_rent_ability(self, val: bool) -> None:
        """
        Sets the rent ability status for the renter.

        Args:
            val (bool): Rental status.
        """
        self.canRent = val


class CompanyWorker(User):
    def __init__(self, id: int) -> None:
        """
        Initializes the CompanyWorker object.
        """
        super().__init__(id)
        self.position: str | None = None
        self.isActive: bool | None = None
        self.load_info()

    def load_info(self):
        """
            Loads worker's information from the database.
        """
        if self.id is not None:
            # Load from database: position and isActive
            pass


class LogIn:
    def __init__(self, login: str, password: str) -> None:
        """
        Enters the system by validating user credentials and loads information.

        Args:
            login (str): User login.
            password (str): Entered password.
        """
        self.creds: Credential = Credential(login, password)
        id: int | None = self.creds.get_id()
        if id is not None:
            # Determine the user type - client or employee
            if True:  # For now, all are clients
                self.user: User = Renter(id)
            else:
                self.user: User = CompanyWorker(id)


class Registration:
    def __init__(self, args: Dict[str, str]) -> None:
        """
        Initializes the Registration object with user information.

        Args:
            args (Dict[str, str]): Dictionary containing information for registration.
        """
        self.user: Renter = Renter()
        self.user.register(args)
