from django.db import models


# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.first_name[0]}. {self.last_name}"

# class PersonalInfo(models.Model):
#     person = models.OneToOneField(
#         Person, on_delete=models.CASCADE, related_name="personal_info"
#     )
#     age = models.IntegerField(null=True, blank=True)
#     job = models.CharField(max_length=15, null=True, blank=True)
#
#     def __str__(self):
#         return f"Info for {self.person}"
