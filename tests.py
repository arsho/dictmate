import unittest
from app import app

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.tester = app.test_client(self)

    def tearDown(self):
        with app.app_context():
            pass

    def test_index(self):
        error_message = "test_index is failed."
        expected_response = b'Dictmate'
        response = self.tester.get('/',
                               follow_redirects=True)
        self.assertEqual(response.status, '200 OK')
        self.assertIn(expected_response,response.data,error_message)

if __name__ == '__main__':
    unittest.main()
