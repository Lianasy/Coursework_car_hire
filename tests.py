import unittest
from datetime import datetime
from unittest.mock import MagicMock

from dateutil.relativedelta import relativedelta

from Users import BaseInfo, Credential, PrivateInfo, User, Renter, CompanyWorker, LogIn, Registration
import io
import sys
from registration_logging import LoggingInterface
import tkinter as tk
class TestBaseInfo(unittest.TestCase):

    def test_initialization(self):
        user_info = BaseInfo(14, "John", "Doe", datetime(1990, 1, 1))
        self.assertEqual(user_info.id, 14)
        self.assertEqual(user_info.firstName, "John")
        self.assertEqual(user_info.lastName, "Doe")
        self.assertEqual(user_info.birthDate, datetime(1990, 1, 1))

    def test_load_from_database(self):
        user_info = BaseInfo(14)
        user_info.load_from_database()
        self.assertEqual(user_info.__dict__, {'id': 14, 'firstName': 'John', 'lastName': 'Doe',
                                              'birthDate': datetime(1990, 1, 1).date()})


class TestCredential(unittest.TestCase):

    def setUp(self):
        # Встановлюємо початкові значення для тестів
        self.credential = Credential("John", "Doe")

    def test_initialization(self):
        self.assertEqual(self.credential.login, "John")
        self.assertEqual(self.credential.password_to_validate, "Doe")

    def test_load_from_database_success(self):
        success = self.credential.load_from_database()
        self.assertTrue(success)
        self.assertEqual(self.credential.login, "John")

    def test_load_from_database_failure(self):
        # Модифікуємо об'єкт, щоб вимусити виняток при завантаженні з бази
        self.credential.login = None
        success = self.credential.load_from_database()
        self.assertFalse(success)

    def test_get_id_valid_password(self):
        self.credential.password_to_validate = "Doe"
        user_id = self.credential.get_id()
        self.assertEqual(user_id, 14)

    def test_get_id_invalid_password(self):
        self.credential.password_to_validate = "wrong_password"
        user_id = self.credential.get_id()
        self.assertIsNone(user_id)


class TestPrivateInfo(unittest.TestCase):

    def setUp(self):
        # Встановлюємо початкові значення для тестів
        self.private_info = PrivateInfo()

    def test_initialization_with_id(self):
        private_info = PrivateInfo(id=1)
        self.assertEqual(private_info.id, 1)

    def test_initialization_without_id(self):
        self.assertIsNone(self.private_info.id)

    def test_load_from_database_success(self):
        info = self.private_info.load_from_database()
        self.assertIsInstance(info, dict)


class TestUser(unittest.TestCase):

    def setUp(self):
        # Встановлюємо початкові значення для тестів
        self.user = User(id=1)

    def test_initialization_with_credentials(self):
        creds = Credential(login='test_login', password='test_password')
        user_with_creds = User(id=2, creds=creds)
        self.assertEqual(user_with_creds.id, 2)
        self.assertEqual(user_with_creds.creds, creds)

    def test_load_private_info_with_id(self):
        self.user.load_private_info()
        self.assertIsNotNone(self.user.privateInfo)

    def test_load_private_info_without_id(self):
        user_without_id = User(id=None)
        user_without_id.load_private_info()
        self.assertIsNone(user_without_id.privateInfo)

    def test_load_base_info_with_id(self):
        self.user.load_base_info()
        self.assertIsNotNone(self.user.baseInfo)

    def test_load_base_info_without_id(self):
        user_without_id = User(id=None)
        user_without_id.load_base_info()
        self.assertIsNone(user_without_id.baseInfo)




class TestRenter(unittest.TestCase):

    def setUp(self):
        # Встановлюємо початкові значення для тестів
        self.renter = Renter(id=14)

    def test_initialization(self):
        self.assertEqual(self.renter.id, 14)
        self.assertIsNone(self.renter.registrationDate)
        self.assertIsNone(self.renter.driverLicenseDate)
        self.assertTrue(self.renter.canRent)

    def test_load_from_database_with_id(self):
        self.renter.load_from_database()
        self.assertIsNotNone(self.renter.baseInfo)
        self.assertIsNotNone(self.renter.privateInfo)
        self.assertIsNotNone(self.renter.registrationDate)
        self.assertIsNotNone(self.renter.driverLicenseDate)


    def test_count_driver_experience(self):
        self.renter.driverLicenseDate = datetime(2007, 1, 17).date()
        experience_delta = relativedelta(datetime.now().date(), self.renter.driverLicenseDate)
        expected_experience = experience_delta.years + experience_delta.months / 12 + experience_delta.days / 365
        self.assertEqual(self.renter.count_driver_experience(), expected_experience)




class TestCompanyWorker(unittest.TestCase):

    def setUp(self):
        # Встановлюємо початкові значення для тестів
        self.worker = CompanyWorker(id=1, creds=Credential('Harry', 'Potter123'))

    def test_initialization(self):
        self.assertEqual(self.worker.id, 1)
        self.assertIsNone(self.worker.position)
        self.assertTrue(self.worker.isActive)

    def test_load_from_database_with_id(self):
        self.worker.load_from_database()
        self.assertIsNotNone(self.worker.baseInfo)
        self.assertIsNotNone(self.worker.privateInfo)
        self.assertIsNotNone(self.worker.position)


class TestLogIn(unittest.TestCase):

    def setUp(self):
        # Встановлюємо початкові значення для тестів
        self.valid_login = "John"
        self.valid_password = "Doe"
        self.invalid_login = "Huisthis"
        self.invalid_password = "invalid_password"
        self.login_instance = LogIn(self.valid_login, self.valid_password)

    def test_successful_login_client(self):
        # Симулюємо успішний логін клієнта
        self.login_instance.creds.get_id = lambda: 14  # Симулюємо існуючий ID
        self.login_instance.user.load_from_database = lambda: None  # Не обов'язково для тестування
        self.login_instance.user = Renter(id=14)  # Симулюємо клієнта
        self.assertIsNone(self.login_instance.user.baseInfo)  # Перевіряємо, що інформація не завантажена перед логіном
        self.login_instance.__init__(self.valid_login, self.valid_password)  # Заново логінимося
        self.assertIsNotNone(self.login_instance.user.baseInfo)  # Перевіряємо, що інформація завантажена після логіну

    def test_successful_login_employee(self):
        # Симулюємо успішний логін працівника
        self.login_instance.creds.get_id = lambda: 2  # Симулюємо існуючий ID
        self.login_instance.user.load_from_database = lambda: None  # Не обов'язково для тестування
        self.login_instance.user = CompanyWorker(id=2)  # Симулюємо працівника
        self.assertIsNone(self.login_instance.user.baseInfo)  # Перевіряємо, що інформація не завантажена перед логіном
        self.login_instance.__init__(self.valid_login, self.valid_password)  # Заново логінимося
        self.assertIsNotNone(self.login_instance.user.baseInfo)  # Перевіряємо, що інформація завантажена після логіну




class TestLoggingInterface(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.config = {'button_width_ratio': 0.2, 'button_height_ratio': 0.1, 'background_color': 'white'}
        self.logging_interface = LoggingInterface(self.root, self.config)

    def tearDown(self):
        self.root.destroy()

    def test_clear_interface(self):
        self.logging_interface.clear_interface()
        self.assertEqual(len(self.root.winfo_children()), 0)

    def test_logging_user(self):
        self.logging_interface.logging_user()

    def test_create_account(self):
        self.logging_interface.create_account()

    def test_process_login(self):
        self.logging_interface.entry_login = MagicMock()
        self.logging_interface.entry_login.get.return_value = "test_login"
        self.logging_interface.entry_password = MagicMock()
        self.logging_interface.entry_password.get.return_value = "test_password"
        self.logging_interface.process_login()



if __name__ == '__main__':
    unittest.main()
