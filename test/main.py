import unittest
import requests
import logging

logger = logging.getLogger(__name__)


class TestRegister(unittest.TestCase):
    base_url = "http://localhost:8000/api/v1"

    def test_0_register(self):
        resp = requests.post(f'{self.base_url}/account/register', json={
            'email': 'test@gmail.com',
            'first_name': 'John',
            'last_name': 'Smith',
            'password': '12345678QWERTY',
        })
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json().get('success'))


class TestLoginAndGetProfile(unittest.TestCase):
    base_url = "http://localhost:8000/api/v1"

    def setUp(self) -> None:
        """ Test case login
        """
        resp = requests.post(f'{self.base_url}/account/login', json={
            'email': 'test@gmail.com',
            'password': '12345678QWERTY',
        })
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json().get('success'))
        self.token = resp.json().get('token')


    def test_1_get_user_profile(self):
        resp = requests.get(f'{self.base_url}/account/profile/me', headers={
            'Authorization': f'Bearer {self.token}'
        })
        print(self.token)
        print(resp.json())
        self.assertTrue(resp.status_code, 200)
        self.assertTrue(resp.json().get('success'))


if __name__ == '__main__':
    unittest.main()

