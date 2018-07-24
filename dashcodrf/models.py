from django.contrib.auth.models import User
from django.db import models


# Client
class Client(models.Model):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    phone_number = models.CharField(max_length=12, unique=True)
    email = models.CharField(max_length=128, unique=True)
    dob = models.DateField()
    national_id = models.IntegerField(unique=True)
    added_on = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    slug = models.SlugField(max_length=128, db_index=True)

    def __str__(self):
        return self.first_name


# Branch
class Branch(models.Model):
    name = models.CharField(max_length=55, unique=True)
    created_by = models.ForeignKey(User, models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    slug = models.SlugField(max_length=128, db_index=True)

    def __str__(self):
        return self.name


# Branch staff
class BranchUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, models.CASCADE, related_name='assigned_by')
    added_on = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    slug = models.SlugField(max_length=128, db_index=True)

    def __str__(self):
        return '%s - %s' % (self.branch.name, self.user.username)


# Plans
class RoutePlan(models.Model):
    title = models.CharField(max_length=55)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    visit_date = models.DateField()
    location = models.CharField(max_length=128, default='Nairobi')
    created_by = models.ForeignKey(User, models.CASCADE, related_name='created_by')
    added_on = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    slug = models.SlugField(max_length=128, db_index=True)

    def __str__(self):
        return self.title


# Plan log
class RoutePlanLog(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    visit_date = models.DateField(auto_now_add=True)
    location_lat = models.CharField(max_length=128)
    location_lon = models.CharField(max_length=128)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    action = models.CharField(max_length=15, default='Account')
    summary = models.TextField(default='Client visit')
    added_on = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    slug = models.SlugField(max_length=128, db_index=True)

    def __str__(self):
        return self.client.first_name


# Account
class Account(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    account_number = models.IntegerField(unique=True)
    created_by = models.ForeignKey(User, models.CASCADE, related_name='opened_by')
    added_on = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    slug = models.SlugField(max_length=128, db_index=True)

    def __str__(self):
        return str(self.account_number)
