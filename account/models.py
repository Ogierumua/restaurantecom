from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, phone_number, password=None):
        if not email: #to make sure the user provides email address
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("user must have  a username")#to make sure the user enters a username
        
        user = self.model(
            email = self.normalize_email(email),# normalizing email address. if 
            username = username,
            first_name = first_name,
            last_name = last_name,
            phone_number = phone_number,
           )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
    
    
    
    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            usernsame = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
         )
        user.is_admin = True
        user.is_active = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
    
    
class User(AbstractBaseUser):
    VENDOR = 1
    CUSTOMER = 2
    
    ROLE_CHOICE = (
        (VENDOR, 'Vendor'),
        (CUSTOMER, 'Customer'),
    )
    first_name = models.CharField(max_length=50)
    last_nane = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=16, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE)
    
    
    #REQUIRED FIELD
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    def get_role(self):
        if self.role == 1:
            user_role = 'vendor'
        elif self.role == 2:
            user_role = 'Customer'
        return user_role
    
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="users/profile_pictures", blank=True, null=True)
    cover_photo = models.ImageField(upload_to="users/cover_photo",blank=True, null=True)
    primaryAddress = models.CharField(max_length=250, blank=True, null=True)
    address_line_1 = models.CharField(max_length=50, blank=True, null=True)
    address_line_2 = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)
    latitude = models.CharField(max_length=50, blank=True, name= True)
    longitude = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    
    
    def full_address(self):
        return f'{self.address_line_1}, {self.address_line_2}'

    def full_address1(self):
        address_parts = [self.address_line_1, self.address_line_2, self.city, self.state, self.country, self.pin_code]
        non_empty_parts = [str(part) for part in address_parts if part]
        return',  '.join(non_empty_parts)

    def __str__(self):
        return self.user.email

    
    
# Create your models here.
