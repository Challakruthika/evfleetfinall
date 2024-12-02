# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# # Custom manager for the User model
# class UserManager(BaseUserManager):
#     def create_user(self, username, email, password=None, role=None):
#         if not email:
#             raise ValueError('The Email field is required')
#         if not username:
#             raise ValueError('The Username field is required')

#         user = self.model(
#             username=username,
#             email=self.normalize_email(email),
#             role=role
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, email, password=None):
#         user = self.create_user(
#             username=username,
#             email=email,
#             password=password,
#             role='fleet_manager'  # Superusers will have the 'fleet_manager' role by default
#         )
#         # user.is_admin = True
#         # user.is_staff = True
#         # user.is_superuser = True
#         user.save(using=self._db)
#         return user

# # Custom User model
# class User(AbstractBaseUser):
#     ROLE_CHOICES = [
#         ('fleet_manager', 'Fleet Manager'),
#         ('driver', 'Driver'),
#     ]
    
#     username = models.CharField(max_length=255, unique=True)
#     email = models.EmailField(max_length=255, unique=True)
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES)
#     #is_active = models.BooleanField(default=True)
#     #is_staff = models.BooleanField(default=False)
#     #is_admin = models.BooleanField(default=False)
#     #is_superuser = models.BooleanField(default=False)

#     # Linking custom manager
#     objects = UserManager()

#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email']

#     class Meta:
#         db_table = 'user_registration_details'  # This will be your custom table name

#     def __str__(self):
#         return self.username


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Custom manager for the User model
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, role=None):
        if not email:
            raise ValueError('The Email field is required')
        if not username:
            raise ValueError('The Username field is required')

        # Create and save a user with the provided details
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            role=role
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        # Create and save a superuser
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            role='fleet_manager'  # Superusers will default to 'fleet_manager' role
        )
        # Uncomment these lines if you want to manually set is_admin, is_staff, etc.
        # user.is_admin = True
        # user.is_staff = True
        # user.is_superuser = True
        user.save(using=self._db)
        return user

# Custom User model
class User(AbstractBaseUser):
    ROLE_CHOICES = [
        ('fleet_manager', 'Fleet Manager'),
        ('driver', 'Driver'),
    ]
    
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    # Additional fields like is_active, is_staff, is_admin, etc., can be added if needed
    # is_active = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=False)
    # is_admin = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=False)

    # Linking custom manager to the model
    objects = UserManager()

    USERNAME_FIELD = 'username'  # Define the username field for authentication
    REQUIRED_FIELDS = ['email']  # Define the required fields for creating a user

    class Meta:
        db_table = 'user_registration_details'  # Name of the table in the database

    def __str__(self):
        return self.username

    # Add any additional methods or properties needed for your user model
