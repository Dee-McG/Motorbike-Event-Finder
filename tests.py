import unittest
import os
from flask_pymongo import PyMongo

import app as app_module

if os.path.exists("env.py"):
    import env

app = app_module.app

# Setting up test DB on Mongo and switching CSRF checks off
app.config["TESTING"] = True
app.config["WTF_CSRF_ENABLED"] = False
app.config['MONGO_URI'] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)
app_module.mongo = mongo


class AppTestCase(unittest.TestCase):
    """Clean the DB"""
    def setUp(self):
        self.client = app.test_client()
        with app.app_context():
            mongo.db.users.delete_many({})
            mongo.db.events.delete_many({})


class AppTests(AppTestCase):
    """Test Home page load"""
    def test_index(self):
        res = self.client.get('/')
        data = res.data.decode('utf-8')
        assert res.status == '200 OK'
        assert 'Motorbike Event Finder' in data

    def test_event_page(self):
        """Test Event Page load"""
        res = self.client.get('/events')
        data = res.data.decode('utf-8')
        assert res.status == '200 OK'
        assert 'Upcoming Events' in data

    def test_contact_page(self):
        """Test Contact Page load"""
        res = self.client.get('/contact')
        data = res.data.decode('utf-8')
        assert res.status == '200 OK'
        assert 'Contact Us' in data

    def test_signup_page(self):
        """Test Sign Up Page load"""
        res = self.client.get('/signup')
        data = res.data.decode('utf-8')
        assert res.status == '200 OK'
        assert 'Sign Up' in data

    def test_signin_page(self):
        """Test Sign In Page load"""
        res = self.client.get('/signup')
        data = res.data.decode('utf-8')
        assert res.status == '200 OK'
        assert 'Sign Up' in data

    def test_signup_functionality(self):
        """Test signup"""
        res = self.client.post('/signup', data=dict(
            username='orange',
            password='123Orange',
            name='Orange'
        ))
        data = res.data.decode('utf-8')
        assert 'orange' in data


class LoggedInTests(AppTestCase):
    """Separate class to clean DB with no cross referencing"""
    def setUp(self):
        """
        Clean the DB, add new user and event and check user and new event
        shows on profile after redirect
        """
        super().setUp()
        res = self.client.post('/signup', data=dict(
            username='orange',
            password='123Orange',
            name='Orange'
        ))
        res = self.client.post('/create-event',
                               follow_redirects=True, data=dict(
                                   event_type='Rally',
                                   location='Letterkenny',
                                   date='30 September 2020',
                                   description='Test',
                                   organiser='Unicorn MCC'
                               ))

        data = res.data.decode('utf-8')
        assert 'orange' in data
        assert 'Rally' in data

    def test_signin_functionality(self):
        """Test Successful Sign in functionality"""
        res = self.client.post('/signin',
                               follow_redirects=True, data=dict(
                                   username='orange',
                                   password='123Orange',
                               ))
        data = res.data.decode('utf-8')
        assert 'Profile' in data
        assert 'Username: orange' in data

    def test_create_event(self):
        """Test event creation functionality"""
        res = self.client.post('/create-event',
                               follow_redirects=True, data=dict(
                                   event_type='Rally',
                                   location='Letterkenny',
                                   date='30 September 2020',
                                   description='Test',
                                   organiser='Unicorn MCC'
                               ))

        data = res.data.decode('utf-8')
        assert 'orange' in data
        assert 'Rally' in data

    def test_edit_event(self):
        """Test event edit functionality"""
        event = mongo.db.events.find_one()
        ids = event.get('_id')
        res = self.client.post('/edit-event/{}'.format(ids),
                               follow_redirects=True, data=dict(
                                   event_type='Club Hosted Event',
                                   location='Letterkenny',
                                   date='20 September 2020',
                                   description='Test',
                                   organiser='Unicorn MCC'
                               ))

        data = res.data.decode('utf-8')
        assert res.status == '200 OK'
        assert 'Club Hosted Event' in data

