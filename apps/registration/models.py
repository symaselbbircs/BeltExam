from __future__ import unicode_literals
from django.db import models
import bcrypt

class UserManager(models.Manager):
    def register(self,**kwargs):
        import re
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-0\._-]+\.[a-zA-Z]*$')
        errors = False
        error_list = []

        # email validate it's an actual email
        if not EMAIL_REGEX.match(kwargs['email']):
            errors = True
            error_list.append("Email address is not valid!")

        #first name no fewer than 2 characters; letters only
        if len(kwargs['first_name']) < 2:
            errors = True
            error_list.append('First name cannot be less than 2 characters!')
        if not kwargs['first_name'].isalpha() and len(kwargs['first_name']) != 0:
            errors = True
            error_list.append("First name contains non-alpha characters!")

        #TODO last name same as first name
        if len(kwargs['last_name']) < 2:
            errors = True
            error_list.append('Last name cannot be less than 2 characters!')
        if not kwargs['last_name'].isalpha() and len(kwargs['last_name']) != 0:
            errors = True
            error_list.append("Last name contains non-alpha characters!")

        #TODO password no fewer than 8 characters in length; matches password confirmation
        if len(kwargs['password1']) < 8:
            errors = True
            error_list.append("Password must be at least 8 characters!")

        if kwargs['password1'] != kwargs['password2']:
            errors = True
            error_list.append("Passwords do not match!")

        return (errors, error_list)

    def create_password(self, password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def verify_password(self, user_pw, db_pw):
        if db_pw == bcrypt.hashpw(user_pw.encode(),db_pw.encode()):
            return True
        else:
            return False


class Users(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length= 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    class Meta:
        managed = False
        db_table = 'users'
