from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.db.models.signals import post_save


# Create your models here.



choices = (('sea', 'sea'), ('waterfront', 'waterfront'))


class Availability(models.Model):
    room_type = models.CharField(max_length=50)
    type_of_View = models.CharField(
        choices=choices, max_length=50, default="sea")

    def __str__(self):
        return self.room_type


class Rooms(models.Model):
  room_type = models.ForeignKey(
      to=Availability, on_delete=models.SET_DEFAULT, default="none")
  price = models.FloatField()
  max_person = models.IntegerField()
  beds = models.IntegerField()
  is_available = models.BooleanField(default=True)



class CustomUser(AbstractUser):
    identification=models.CharField(max_length=255)
    gender=models.CharField(max_length=255, default="male")


class Booking(models.Model):
    room = models.ForeignKey(
        to=Rooms, on_delete=models.SET_NULL, max_length=50, null=True, related_name="room_booking")
    checkin = models.DateTimeField(default=datetime.datetime.now())
    checkout = models.DateTimeField(default=datetime.datetime.now())
    numberguests = models.IntegerField()
    name = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

def check_availability():
    if room_booking.checkin > datetime.datetime.now():
        is_available = False
    elif room_booking.checkout > datetime.datetime.now():
        is_available = True
    else:
        is_available = True
        
post_save.connect(check_availability, sender=Booking)






class Profile(models.Model):
    user = models.OneToOneField(to=CustomUser, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    nationality = models.CharField(max_length=100)
    id_or_passport = models.ImageField(upload_to='id_or_passport', blank=True, null=True)
    visa_card_number = models.CharField(max_length=16, blank=True, null=True)
    visa_card_expiry = models.DateField(blank=True, null=True)


#Autogenerate Profile after User SignUp
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

post_save.connect(create_profile,sender=CustomUser)




    




