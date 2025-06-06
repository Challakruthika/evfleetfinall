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


from django.contrib.auth.models import AbstractUser
from django.db import models
from ev_fleet_management.supabase_utils import create_user, update_user, delete_user

class User(AbstractUser):
    ROLE_CHOICES = (
        ('fleet_manager', 'Fleet Manager'),
        ('driver', 'Driver'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    class Meta:
        db_table = 'user_registration_details'

    def save(self, *args, **kwargs):
        # Prepare user data for Supabase
        user_data = {
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'is_active': self.is_active,
            'is_staff': self.is_staff,
            'is_superuser': self.is_superuser,
        }

        if not self.pk:  # New user
            # Create user in Supabase
            response = create_user(user_data)
            if response.data:
                self.pk = response.data[0]['id']
        else:  # Existing user
            # Update user in Supabase
            update_user(str(self.pk), user_data)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete user from Supabase
        delete_user(str(self.pk))
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    # Add any additional methods or properties needed for your user model
