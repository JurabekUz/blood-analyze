from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    MALE = 'M'
    FEMALE = 'F'
    genders = {MALE: "Male", FEMALE: "Female"}

    ADMIN = 'admin'
    DOCTOR = 'doctor'
    roles = {DOCTOR: "Doctor", ADMIN: "Admin"}

    role = models.CharField(max_length=10, choices=roles)
    father_name = models.CharField(max_length=50)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=genders)

    class Meta:
        ordering = ['-id']

    REQUIRED_FIELDS = ["role", 'gender']

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s %s" % (self.first_name, self.last_name, self.father_name)
        return full_name.strip()

    @property
    def age(self):
        """Return age computed from birthday."""
        if not self.birthday:
            return None

        today = timezone.now().date()

        years = today.year - self.birthday.year
        if (today.month, today.day) < (self.birthday.month, self.birthday.day):
            years -= 1

        return years

