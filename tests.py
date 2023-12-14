import unittest
from datetime import datetime
from Users import BaseInfo, Credential, PrivateInfo, User, Renter, CompanyWorker, LogIn, Registration
import io
import sys

class TestBaseInfo(unittest.TestCase):

    def test_initialization(self):
        user_info = BaseInfo(1, "John", "Doe", datetime(1990, 5, 7))
        self.assertEqual(user_info.id, 1)
        self.assertEqual(user_info.firstName, "John")
        self.assertEqual(user_info.lastName, "Doe")
        self.assertEqual(user_info.birthDate, datetime(1990, 5, 7))

    def test_upload_to_database_new_success(self):
        user_info = BaseInfo(1, "John", "Doe", datetime(1990, 5, 7))
        success = user_info.upload_to_database_new()
        self.assertTrue(success)

    def test_upload_to_database_existing_success(self):
        user_info = BaseInfo(1, "John", "Doe", datetime(1990, 5, 7))
        success = user_info.upload_to_database_existing()
        self.assertTrue(success)

    def test_load_from_database(self):
        user_info = BaseInfo(1)
        user_info.load_from_database()
        self.assertEqual(user_info.__dict__, {'id': 1, 'firstName': 'testFirstName', 'lastName': 'testLastName',
                                              'birthDate': datetime(1990, 5, 7)})


class TestCredential(unittest.TestCase):

    def setUp(self):
        # Встановлюємо початкові значення для тестів
        self.credential = Credential("test_login", "test_password")

    def test_initialization(self):
        self.assertEqual(self.credential.login, "test_login")
        self.assertEqual(self.credential.password_to_validate, "test_password")

    def test_load_from_database_success(self):
        success = self.credential.load_from_database(1)
        self.assertTrue(success)
        self.assertEqual(self.credential.login, "testlogin")

    def test_load_from_database_failure(self):
        # Модифікуємо об'єкт, щоб вимусити виняток при завантаженні з бази
        self.credential.login = None
        success = self.credential.load_from_database(1)
        self.assertFalse(success)

    def test_get_id_valid_password(self):
        self.credential.password_to_validate = "test_password"
        user_id = self.credential.get_id()
        self.assertEqual(user_id, 1)

    def test_get_id_invalid_password(self):
        self.credential.password_to_validate = "wrong_password"
        user_id = self.credential.get_id()
        self.assertIsNone(user_id)

    def test_update_login_success(self):
        success = self.credential.update_login("new_login")
        self.assertTrue(success)
        self.assertEqual(self.credential.login, "new_login")

    def test_update_login_failure(self):
        success = self.credential.update_login(None)
        self.assertFalse(success)

    def test_update_password_success(self):
        success = self.credential.update_password("new_password")
        self.assertTrue(success)

    def test_update_password_failure(self):
        success = self.credential.update_password(None)
        self.assertFalse(success)

    def test_upload_to_database_new_success(self):
        success = self.credential.upload_to_database_new("new_password", 1)
        self.assertTrue(success)

    def test_upload_to_database_new_failure(self):
        success = self.credential.upload_to_database_new(None, 1)
        self.assertFalse(success)


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
        self.assertIn('photo', info)
        self.assertIn('passport', info)

    def test_upload_to_database_new_success(self):
        args = {'photo': 'new_photo', 'passport': '12345678'}
        user_id = self.private_info.upload_to_database_new(args)
        self.assertEqual(self.private_info.id, user_id)

    def test_upload_to_database_new_failure(self):
        # Модифікуємо об'єкт, щоб вимусити виняток при вивантаженні в базу
        self.private_info.id = 1
        args = {'photo': 'new_photo', 'passport': '12345678'}
        user_id = self.private_info.upload_to_database_new(args)
        self.assertEqual(user_id, -1)

    def test_upload_to_database_existing_success(self):
        args = {'photo': 'new_photo', 'passport': '12345678'}
        success = self.private_info.upload_to_database_existing(args)
        self.assertTrue(success)

    def test_upload_to_database_existing_failure(self):
        # Модифікуємо об'єкт, щоб вимусити виняток при вивантаженні в базу
        args = {'photo': 'new_photo', 'passport': '12345678'}
        success = self.private_info.upload_to_database_existing(args)
        self.assertFalse(success)


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

    def test_change_base_info(self):
        new_info = {'firstName': 'John', 'lastName': 'Doe', 'birthDate': datetime(1990, 5, 7)}
        self.user.load_base_info()
        self.user.change_base_info(new_info)
        self.assertEqual(self.user.baseInfo.firstName, 'John')
        self.assertEqual(self.user.baseInfo.lastName, 'Doe')
        self.assertEqual(self.user.baseInfo.birthDate, datetime(1990, 5, 7))

    def test_change_private_info(self):
        new_info = {'photo': 'new_photo', 'passport': '12345678'}
        self.user.privateInfo = PrivateInfo()
        self.user.change_private_info(new_info)
        self.assertIsNotNone(self.user.privateInfo)

    def test_change_credentials(self):
        new_info = {'login': 'new_login', 'password': 'new_password'}
        self.user.creds = Credential(login='old_login', password='old_password')
        self.user.change_credentials(new_info)
        self.assertEqual(self.user.creds.login, 'new_login')
        self.assertEqual(self.user.creds.password_to_validate, 'new_password')


class TestRenter(unittest.TestCase):

    def setUp(self):
        # Встановлюємо початкові значення для тестів
        self.renter = Renter(id=1)

    def test_initialization(self):
        self.assertEqual(self.renter.id, 1)
        self.assertIsNone(self.renter.registrationDate)
        self.assertIsNone(self.renter.driverLicenseDate)
        self.assertTrue(self.renter.canRent)

    def test_load_from_database_with_id(self):
        self.renter.load_from_database()
        self.assertIsNotNone(self.renter.baseInfo)
        self.assertIsNotNone(self.renter.privateInfo)
        self.assertIsNotNone(self.renter.registrationDate)
        self.assertIsNotNone(self.renter.driverLicenseDate)

    def test_register_successful(self):
        args = {
            'privateInfo': {'photo': 'test_photo', 'passport': '12345678'},
            'baseInfo': {'firstName': 'John', 'lastName': 'Doe', 'birthDate': datetime(1990, 5, 7)},
            'driverLicenseDate': datetime(2022, 1, 1),
            'credentials': {'login': 'test_login', 'password': 'test_password'}
        }
        self.assertTrue(self.renter.register(args))
        self.assertIsNotNone(self.renter.baseInfo)
        self.assertIsNotNone(self.renter.privateInfo)
        self.assertIsNotNone(self.renter.registrationDate)
        self.assertIsNotNone(self.renter.driverLicenseDate)
        self.assertIsNotNone(self.renter.creds)

    def test_register_failure(self):
        # Simulate a failure during registration
        args = {
            'privateInfo': {'photo': 'test_photo', 'passport': '12345678'},
            'baseInfo': {'firstName': 'John', 'lastName': 'Doe', 'birthDate': datetime(1990, 5, 7)},
            'driverLicenseDate': datetime(2022, 1, 1),
            'credentials': {'login': 'test_login', 'password': 'test_password'}
        }
        self.assertFalse(self.renter.register(args))
        self.assertIsNone(self.renter.baseInfo)
        self.assertIsNone(self.renter.privateInfo)
        self.assertIsNone(self.renter.registrationDate)
        self.assertIsNone(self.renter.driverLicenseDate)
        self.assertIsNone(self.renter.creds)

    def test_count_driver_experience(self):
        self.renter.driverLicenseDate = datetime(2022, 1, 1).date()
        expected_experience = datetime.now().date() - self.renter.driverLicenseDate
        self.assertEqual(self.renter.count_driver_experience(), expected_experience)

    def test_count_time_in_system(self):
        self.renter.registrationDate = datetime(2022, 1, 1).date()
        expected_time_in_system = datetime.now().date() - self.renter.registrationDate
        self.assertEqual(self.renter.count_time_in_system(), expected_time_in_system)

    def test_set_rent_ability(self):
        self.renter.set_rent_ability(False)
        self.assertFalse(self.renter.canRent)


class TestCompanyWorker(unittest.TestCase):

    def setUp(self):
        # Встановлюємо початкові значення для тестів
        self.worker = CompanyWorker(id=1, creds=Credential('login1', 'password1'))

    def test_initialization(self):
        self.assertEqual(self.worker.id, 1)
        self.assertIsNone(self.worker.position)
        self.assertTrue(self.worker.isActive)

    def test_load_from_database_with_id(self):
        self.worker.load_from_database()
        self.assertIsNotNone(self.worker.baseInfo)
        self.assertIsNotNone(self.worker.privateInfo)
        self.assertIsNotNone(self.worker.position)

    def test_change_base_info_successful(self):
        self.worker.load_from_database()
        new_info = {'firstName': 'New', 'lastName': 'Name', 'birthDate': datetime(1995, 1, 1)}
        self.worker.change_base_info(new_info)
        self.assertEqual(self.worker.baseInfo.firstName, new_info['firstName'])
        self.assertEqual(self.worker.baseInfo.lastName, new_info['lastName'])
        self.assertEqual(self.worker.baseInfo.birthDate, new_info['birthDate'])

    def test_change_base_info_failure(self):
        self.worker.load_from_database()
        # Simulate a failure during change_base_info
        self.worker.baseInfo.upload_to_database_existing = lambda: False  # Simulate failure
        new_info = {'firstName': 'New', 'lastName': 'Name', 'birthDate': datetime(1995, 1, 1)}
        self.worker.change_base_info(new_info)
        # Ensure that the baseInfo attributes remain unchanged
        self.assertIsNotNone(self.worker.baseInfo)
        self.assertNotEqual(self.worker.baseInfo.firstName, new_info['firstName'])
        self.assertNotEqual(self.worker.baseInfo.lastName, new_info['lastName'])
        self.assertNotEqual(self.worker.baseInfo.birthDate, new_info['birthDate'])

    def test_change_private_info_successful(self):
        self.worker.load_from_database()
        new_info = {'photo': 'new_photo', 'passport': 'new_passport'}
        self.worker.change_private_info(new_info)
        self.assertEqual(self.worker.privateInfo.load_from_database(), new_info)

    def test_change_private_info_failure(self):
        self.worker.load_from_database()
        # Simulate a failure during change_private_info
        self.worker.privateInfo.upload_to_database_existing = lambda args: False  # Simulate failure
        new_info = {'photo': 'new_photo', 'passport': 'new_passport'}
        self.worker.change_private_info(new_info)
        # Ensure that the privateInfo attributes remain unchanged
        self.assertNotEqual(self.worker.privateInfo.load_from_database(), new_info)

    def test_change_credentials_successful(self):
        new_info = {'login': 'new_login', 'password': 'new_password'}
        self.worker.change_credentials(new_info)
        self.assertEqual(self.worker.creds.login, new_info['login'])
        self.assertEqual(self.worker.creds.get_id(), self.worker.id)

    def test_change_credentials_failure(self):
        # Simulate a failure during change_credentials
        self.worker.creds.update_password = lambda new_password: False  # Simulate failure
        new_info = {'login': 'new_login', 'password': 'new_password'}
        self.worker.change_credentials(new_info)
        # Ensure that the credentials remain unchanged
        self.assertNotEqual(self.worker.creds.login, new_info['login'])
        self.assertFalse(self.worker.creds.__to_valid_password())


class TestLogIn(unittest.TestCase):

    def setUp(self):
        # Встановлюємо початкові значення для тестів
        self.valid_login = "test_user"
        self.valid_password = "test_password"
        self.invalid_login = "invalid_user"
        self.invalid_password = "invalid_password"
        self.login_instance = LogIn(self.valid_login, self.valid_password)

    def test_successful_login_client(self):
        # Симулюємо успішний логін клієнта
        self.login_instance.creds.get_id = lambda: 1  # Симулюємо існуючий ID
        self.login_instance.user.load_from_database = lambda: None  # Не обов'язково для тестування
        self.login_instance.user = Renter(id=1)  # Симулюємо клієнта
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

    def test_unsuccessful_login(self):
        # Симулюємо невдалий логін
        new_login_instance = LogIn(self.invalid_login, self.invalid_password)
        self.assertNotIn('user', dir(new_login_instance))  # Перевіряємо, що користувач не залогінений


class TestRegistration(unittest.TestCase):

    def setUp(self):
        # Встановлюємо початкові значення для тестів
        self.valid_args = {
            'privateInfo': {'photo': 'photo1', 'passport': '11111111'},
            'baseInfo': {'firstName': 'John', 'lastName': 'Doe', 'birthDate': '1990-01-01'},
            'driverLicenseDate': '2020-01-01',
            'credentials': {'login': 'john_doe', 'password': 'secure_password'}
        }
        self.invalid_args = {}  # Порожній словник, щоб викликати помилку під час реєстрації
        self.held_output = io.StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_successful_registration(self):
        # Симулюємо успішну реєстрацію
        registration_instance = Registration(self.valid_args)
        self.assertTrue(registration_instance.user.canRent)  # Перевіряємо, що користувач створений

    def test_unsuccessful_registration(self):
        Registration(self.invalid_args)
        self.held_output.seek(0)
        output_text = self.held_output.read().strip()
        expected_output = 'Can`t register.'
        self.assertEqual(output_text, expected_output)


if __name__ == '__main__':
    unittest.main()
