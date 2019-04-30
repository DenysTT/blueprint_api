from flask import Blueprint, request, jsonify
from app.models.mongo_model import User
from datetime import datetime
import logging

log = logging.getLogger(__name__)
logpattern = '%(asctime)s %(levelname)s %(message)s'
log_handler = logging.StreamHandler()
log_handler.setFormatter(logging.Formatter(logpattern))
log.addHandler(log_handler)
log.setLevel(logging.DEBUG)

api = Blueprint('api', __name__)


@api.route('/hello/<username>', methods=['PUT', 'GET'])
def put_user_birthday(username=None):
    """Api call which serves both PUT and GET methods, in case of PUT will create/update user with Birthday date in DB
    will also validate wrong specified date/name, 'GET' request will display days till user's birthday"""

    if not username.isalpha():
        return 'Username %s must contain only letters' % username, 400
    if request.method == 'PUT':
        try:
            date = datetime.strptime(request.values['DateOfBirth'], "%d-%m-%Y").date()
        except ValueError:
            log.error('The date %s is invalid,please use "dd-mm-yyyy" format' % (request.values['DateOfBirth']))
            return 'The date %s is invalid,please use "dd-mm-yyyy" format' % (request.values['DateOfBirth']), 400
        except KeyError as e:
            log.debug('"DateOfBirth" data key is absent in request')
            return 'You must use proper data key "DateOfBirth"', 400
        if check_if_date_is_greater_than_today(date):
            return 'DateOfBirth date must not be greater than today', 400
        save_user_to_db(username, date)
        return '', 204
    elif request.method == 'GET':
        today = datetime.today()
        result = User.objects(user_name=username).first()
        if result:
            if is_birthday_today(result.birthdate, today):
                return jsonify(message='Hello, %s! Happy Birthday!' % username)
            else:
                return jsonify(message='Hello, %s! Your birthday is in %d day(s)' % (username, count_days_to_birthday(
                    result.birthdate, today)))
        else:
            return 'User %s is absent' % username


def is_birthday_today(original_date, today):
    """Function which returns True if today is Birthday of a user"""
    return original_date.day == today.day and original_date.month == today.month


def count_days_to_birthday(original_date, now):
    """Function which counts days till next birthday"""
    delta1 = datetime(now.year, original_date.month, original_date.day)
    delta2 = datetime(now.year+1, original_date.month, original_date.day)
    return (min(delta1, delta2) - now).days


def save_user_to_db(username, birthday):
    """Function will create/update user in DB"""
    try:
        User(user_name=username,
             birthdate=birthday).save()
        log.info('User %s was created' % username)
    except Exception as e:
        log.error("Error \n %s" % e)


def check_if_date_is_greater_than_today(date):
    """Function which validate date"""
    now = datetime.now().date()
    return date > now

