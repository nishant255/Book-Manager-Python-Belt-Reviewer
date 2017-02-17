from __future__ import unicode_literals
from django.contrib import messages
from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
NAME_REGEX = re.compile(r'/^[a-zA-Z]+', re.MULTILINE)
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*(_|[^\w])).+$', re.MULTILINE)

# ==============================================================================
#                            MANAGER CLASSES
# ==============================================================================

# ------------------------------------------------------------------------------
#                              USER MANAGER
# ------------------------------------------------------------------------------

class UserManager(models.Manager):

# ---------------------------
#    Registration Validator
# ---------------------------

    def reg_validator(self,POST):
        valid = True
        error_list = []
        first_name = POST['first_name'].lower()
        last_name = POST['last_name'].lower()
        email = POST['email'].lower()
        password = POST['password'].encode()
        passconf = POST['passconf']

        email_check = User.objects.filter(email=POST['email'])
        if email_check:
            error_list.append('Invalid Email')
            return False, error_list

# Checking FIRST NAME
        if len(first_name) < 2:
            error_list.append('First Name cannot be less than 2 Characters')
            valid = False
        if not first_name.isalpha():
            error_list.append('First Name cannot contain Numbers or Blank Spaces')
            valid = False

# Checking LAST NAME
        if len(last_name) < 2:
            error_list.append('Last Name cannot be less than 2 Characters')
            valid = False
        if not  last_name.isalpha():
            error_list.append('Last Name cannot contain Numbers or Blank Spaces')
            valid = False

# Checking EMAIL
        if len(email) < 5:
            error_list.append('Email Too Short')
            valid = False
        if not EMAIL_REGEX.match(email):
            error_list.append('Invalid Email')
            valid = False

# Checking PASSWORD
        if len(password) < 8:
            error_list.append('Password cannot be less than 8 Characters')
            valid = False
        if not PASSWORD_REGEX.match(password):
            error_list.append('Password Requires atleast One Uppercase, One Lowercase, One Number and One Symbol')
            valid = False
        if password != passconf:
            error_list.append("Passwords Doesn't Match")
            valid = False

# If any Input Contraint Fails VALID is False
        if not valid:
            return False, error_list

# Creating New User Once all Input Contraint passed and return User object
        password_hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        User.objects.create(first_name=first_name,last_name=last_name,email=email,password=password_hashed)
        user = User.objects.filter(email = email)
        return True, user[0]

# ---------------------------
#       Login Validator
# ---------------------------

    def login_validate(self, POST):
        error_list = []
        email = POST['email'].lower()
        password = POST['password']
        user_pass = User.objects.filter(email=email)

# Checking if User Exist
        if not user_pass:
            error_list.append("Invalid Email or Password")
            return False, error_list

# Checking Password; if True Return With User Object
        confpass = user_pass[0].password
        if bcrypt.hashpw(password.encode(), confpass.encode()) == confpass:
            user = User.objects.filter(email = email)
            return True, user[0]
        else:
            error_list.append('Invalid Email or Password')
            return False, error_list
        return None

# ------------------------------------------------------------------------------
#                              BOOK MANAGER
# ------------------------------------------------------------------------------

class BookManager(models.Manager):

# ---------------------------
#         Adding Book
# ---------------------------

    def adding_book(self, POST, user_id):
        error_list = []
        author = POST['author'].lower()
        author_new = POST['author_new'].lower()
        print author
        title = POST['title'].lower()
        ratings = POST['ratings']
        print ratings
        review = POST['review']
        U1 = User.objects.filter(id = user_id)
        if title == "" or review == "":
            error_list.append("Cannot add book without Title or Review")
            return False, error_list
        if author_new != "":
            A1 = Author.objects.filter(name = author_new)
            if len(A1) < 1:

                A = Author.objects.create(name = author_new)
                A1 = [A]
        else:
            A1 = Author.objects.filter(name = author)

        B1 = Book.objects.filter(title = title)
        if len(B1) < 1:
            B1 = Book.objects.create(title = title, author = A1[0], user = U1[0])
            Review.objects.create(review = review, ratings = ratings,user = U1[0], book = B1)
            return True, B1

        Review.objects.create(review = review,ratings = ratings, user = U1[0], book = B1[0])
        return True, B1[0]



# ------------------------------------------------------------------------------
#                              Review MANAGER
# ------------------------------------------------------------------------------

class ReviewManager(models.Manager):
    def adding_review(self, book_id, user_id, POST):
        error_list = []
        if POST['review'] == "":
            error_list.append("Review cannot be Blank")
            return False, error_list
        U1 = User.objects.get(id = user_id)
        B1 = Book.objects.get(id = book_id)
        Review.objects.create(review = POST['review'], ratings = POST['ratings'], user = U1, book = B1)
        error_list.append("Review added Successfully")
        return True, error_list

# ------------------------------------------------------------------------------
#                              Author MANAGER
# ------------------------------------------------------------------------------

class AuthorManager(models.Manager):
    def adding_author(self):
        pass

# ==============================================================================
#                                CLASS
# ==============================================================================

# ------------------------------------------------------------------------------
#                              User Class
# ------------------------------------------------------------------------------
class User(models.Model):
    first_name = models.CharField(max_length=45, default = "Not Available")
    last_name = models.CharField(max_length=45, default = "Not Available")
    email =  models.CharField(max_length=45)
    password = models.TextField(default = "Not Available")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

# ------------------------------------------------------------------------------
#                              Author Class
# ------------------------------------------------------------------------------

class Author(models.Model):
    name = models.CharField(max_length=45, default = "Not Available")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = AuthorManager()

# ------------------------------------------------------------------------------
#                              Book Class
# ------------------------------------------------------------------------------

class Book(models.Model):
    title = models.CharField(max_length=45, default = "Not Available")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    objects = BookManager()

# ------------------------------------------------------------------------------
#                              Review Class
# ------------------------------------------------------------------------------

class Review(models.Model):
    review = models.TextField()
    ratings = models.IntegerField(null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    objects = ReviewManager()
