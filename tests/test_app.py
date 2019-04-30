import pytest
from flask_mongoengine import MongoEngine
from app import create_app
from mongoengine import connect
from datetime import datetime, timedelta
import os

TEST_DB_NAME = os.getenv('TEST_DB_NAME', 'test_db')


@pytest.fixture(scope="session", autouse=True)
def drop_testdb_before_all_tests():
    # prepare something ahead of all tests
    # in this case test_db should be dropped before triggering tests
    db = connect(TEST_DB_NAME)
    db.drop_database(TEST_DB_NAME)


@pytest.fixture
def client():
    # runs every time before each test
    # in this case db connection will be established with testing params
    app = create_app({
        'TESTING': True,
        'MONGODB_DB': TEST_DB_NAME,
    })

    client = app.test_client()
    with app.app_context():
        MongoEngine(app)
    yield client


def test_check_empty_db(client):
    """Start with a blank database."""
    # Check message if user is absent
    rv = client.get('/hello/Christopher')
    assert b'User Christopher is absent' in rv.data
    assert 200 == rv._status_code


@pytest.mark.parametrize("user_name",['Müller', '张', 'Александр', 'Christopher'])
def test_check_valid_user_name(client, user_name):
    # Check that user with specific names can be created
    rv = client.put('/hello/' + user_name, data={'DateOfBirth': generate_birthday_date(10).strftime("%d-%m-%Y")},
                    follow_redirects=True)
    assert 204 == rv._status_code


def test_check_user_birthday_date(client):
    # Check that if user available in database, days till birthday will displayed
    client.put('/hello/Simon', data={'DateOfBirth': generate_birthday_date(5).strftime("%d-%m-%Y")},
                follow_redirects=True)
    rv = client.get('/hello/Simon')
    assert b'{"message":"Hello, Simon! Your birthday is in 5 day(s)"}\n' in rv.data
    assert 200 == rv._status_code


def test_check_user_update(client):
    # Check that user can be updated
    client.put('/hello/Alejandro', data={'DateOfBirth': generate_birthday_date(9).strftime("%d-%m-%Y")},
                follow_redirects=True)
    client.put('/hello/Alejandro', data={'DateOfBirth': generate_birthday_date(12).strftime("%d-%m-%Y")},
                follow_redirects=True)
    rv = client.get('/hello/Alejandro')

    assert b'{"message":"Hello, Alejandro! Your birthday is in 12 day(s)"}\n' in rv.data


@pytest.mark.parametrize("date_format",['1988-12-01', '12-01-88', '12031988', ''])
def test_check_invalid_date_format(client, date_format):
    # Check that users with wrong formatted birthday date will receive notification
    rv = client.put('/hello/Christopher', data={'DateOfBirth': date_format},
                    follow_redirects=True)

    assert b'The date %s is invalid,please use "dd-mm-yyyy" format' % str.encode(date_format) in rv.data
    assert 400 == rv._status_code


def test_user_cannot_be_created_with_future_date(client):
    # Check that users with birthday date in future cannot be created and
    rv = client.put('/hello/UserWithWrongBirthdayDate', data={'DateOfBirth': generate_future_date()},
                    follow_redirects=True)
    assert b'DateOfBirth date must not be greater than today' in rv.data
    assert 400 == rv._status_code


def test_check_todays_birthday_message(client):
    # Check that users with today birthday date will be congratulated
    client.put('/hello/Lucky', data={'DateOfBirth': datetime.today().strftime("%d-%m-%Y")},
                follow_redirects=True)
    rv = client.get('/hello/Lucky')

    assert b'{"message":"Hello, Lucky! Happy Birthday!"}\n' in rv.data


@pytest.mark.parametrize("user_name",['Wrong_Name', 'WrongName2', 'Wrong Name'])
def test_check_invalid_user_name(client, user_name):
    # Check that users with symbols/digits in name cannot be created
    rv = client.put('/hello/' + user_name, data={'DateOfBirth': generate_birthday_date(12).strftime("%d-%m-%Y")},
                    follow_redirects=True)
    assert b'Username %s must contain only letters' % str.encode(user_name) in rv.data


def generate_birthday_date(days):
    birthday_date = (datetime.today() + timedelta(days=days) - timedelta(weeks=52))
    return birthday_date


def generate_future_date():
    return (datetime.today() + timedelta(days=1)).strftime("%d-%m-%Y")



