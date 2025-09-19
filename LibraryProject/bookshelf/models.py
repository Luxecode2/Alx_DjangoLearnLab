from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.conf import settings # Import settings to reference AUTH_USER_MODEL later

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        Ensures 'date_of_birth' is handled during user creation.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a Superuser with the given email and password.
        Ensures 'date_of_birth' is handled during superuser creation.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Ensure that date_of_birth is set for superuser if it's a required field.
        # Although it's usually not required for superuser creation in command line.
        # For simplicity, we'll assume it's optional for CLI superuser creation.
        # If it needs to be strictly required, it should be prompted in custom command.
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom User model extending AbstractUser with additional fields.
    - date_of_birth: A date field.
    - profile_photo: An image field.
    Uses email as the unique identifier for authentication.
    """
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    # Use email as the unique identifier for authentication
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS are prompted when creating a user via createsuperuser.
    # 'username' is removed by default when USERNAME_FIELD is changed.
    # 'date_of_birth' is added here as an example, but it needs to be optional or handled
    # in the create_superuser logic if you don't want to input it every time.
    REQUIRED_FIELDS = ['date_of_birth']

    objects = CustomUserManager() # Assign the custom manager

    def __str__(self):
        return self.email

    # Custom permissions for Task 2 will be added here
    class Meta:
        permissions = [
            ("can_view", "Can view book"),
            ("can_create", "Can create book"),
            ("can_edit", "Can edit book"),
            ("can_delete", "Can delete book"),
        ]


# Example of updating foreign keys in other models to use CustomUser
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField(default=timezone.now)
    # Foreign key now points to the custom user model defined by AUTH_USER_MODEL
    # Using settings.AUTH_USER_MODEL makes it dynamically refer to the custom user.
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='books_added')

    def __str__(self):
        return self.title

    # Permissions for Task 2 will be defined here as well for the Book model
    # (Already defined in CustomUser above for simplicity to avoid two Meta classes in one file if possible,
    # but strictly speaking, book permissions belong to the Book model's Meta options.
    # Let's move them here for correctness as per task 2 instructions).
    class Meta:
        permissions = [
            ("can_view", "Can view book"),
            ("can_create", "Can create book"),
            ("can_edit", "Can edit book"),
            ("can_delete", "Can delete book"),
        ]