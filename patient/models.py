from django.db import models
from django.utils import timezone

from users.models import User


class Patient(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    genders = {MALE: "Male", FEMALE: "Female"}

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    father_name = models.CharField(max_length=50)
    birthday = models.DateField()
    gender = models.CharField(max_length=1, choices=genders)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-id']

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s %s" % (self.first_name, self.last_name, self.father_name)
        return full_name.strip()

    @property
    def age(self):
        """Return age computed from birthday."""
        today = timezone.now().date()

        years = today.year - self.birthday.year
        if (today.month, today.day) < (self.birthday.month, self.birthday.day):
            years -= 1

        return years
