import mongoengine


# framework for mapping an object-oriented domain model to a database
class User(mongoengine.Document):
    user_name = mongoengine.StringField(primary_key=True)
    birthdate = mongoengine.DateTimeField()
