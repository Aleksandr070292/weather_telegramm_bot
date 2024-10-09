import unittest
from flask import json
from database import Session, Log
import app

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.session = Session()

    def tearDown(self):
        # Очистка базы данных после каждого теста
        self.session.query(Log).delete()
        self.session.commit()

    def test_get_logs_empty(self):
        response = self.app.get('/logs?page=1&limit=10')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), [])

    def test_get_logs_with_data(self):
        log_entry = Log(user_id=1, command='/weather Москва', response='Погода в Москве: 10°C',
                        timestamp='2024-10-09T10:00:00')
        self.session.add(log_entry)
        self.session.commit()

        response = self.app.get('/logs?page=1&limit=10')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['user_id'], 1)
        self.assertEqual(data[0]['command'], '/weather Москва')

    def test_get_logs_with_filter(self):
        log_entry = Log(user_id=1, command='/weather Москва', response='Погода в Москве: 10°C',
                        timestamp='2024-10-09T10:00:00')
        self.session.add(log_entry)
        self.session.commit()

        response = self.app.get('/logs?page=1&limit=10&start_time=2024-10-09T00:00:00&end_time=2024-10-09T12:00:00')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)

if __name__ == '__main__':
    unittest.main()