import unittest
import requests


class TestPredict(unittest.TestCase):
    def setUp(self):
        self.url = 'http://localhost:5000/predict'
        with open("../data/base64/dog.txt") as file:
            self.image_base64 = file.read().replace('\n', ' ')

    def test_predict(self):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {'image': self.image_base64}
        response = requests.post(self.url, headers=headers, data=data)
        response_json = response.json()
        self.assertTrue(len(response_json) > 0)
        self.assertIn('class_id', response_json[0])
        self.assertIn('class_name', response_json[0])
        self.assertIn('confidence', response_json[0])
        self.assertIn('x_min', response_json[0])
        self.assertIn('y_min', response_json[0])
        self.assertIn('width', response_json[0])
        self.assertIn('height', response_json[0])

if __name__ == '__main__':
    unittest.main()
