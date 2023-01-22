import unittest
from unittest import TestCase
import requests

BASE_URL = "http://localhost:8000/predict"

class ContainerTestCase(TestCase):

    def test_response(self):
        
        image_file = {'image': open('./modelcls/2022-08-02 11_11_17-Smartphone Apple iPhone 11 128GB Black _ Public.png', 'rb')}
        r = requests.post(BASE_URL, files=image_file)
        self.assertEqual(r.status_code, 200)

if __name__ == '__main__':
    unittest.main()