import unittest
import requests
import logging

logger = logging.getLogger(__name__)


class TestDeleteUser(unittest.TestCase):
    base_url = "http://localhost:8000/api/v1"

    def test_0_delete_user(self):
        # login
        resp = requests.post(f'{self.base_url}/account/login', json={
            'email': 'test@gmail.com',
            'password': '12345678QWERTY',
        })
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json().get('success'))
        token = resp.json().get('token')

        # delete user 
        resp = requests.delete(f'{self.base_url}/account/profile/me', headers={
            'Authorization': f'Bearer {token}'
        })
        print(resp.json())
        self.assertEqual(resp.status_code, 200)

    def test_1_register(self):
        resp = requests.post(f'{self.base_url}/account/register', json={
            'email': 'test@gmail.com',
            'first_name': 'John',
            'last_name': 'Smith',
            'password': '12345678QWERTY',
        })
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json().get('success'))


class TestGetProfile(unittest.TestCase):
    base_url = "http://localhost:8000/api/v1"

    def setUp(self):
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

    def test_2_update_user_profile(self):
        resp = requests.put(f'{self.base_url}/account/profile/me', json={
            'first_name': 'Jay',
            'last_name': 'Chou',
            'password': '',
            'bio': 'This is a example bio.',
            'profile_picture': '/static/pics/1.jpg',
        }, headers={
            'Authorization': f'Bearer {self.token}'
        })
        self.assertEqual(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()
