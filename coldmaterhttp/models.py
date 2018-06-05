from django.db import models

class User(models.Model):
	userid    = models.CharField(max_length = 10)
	fname     = models.CharField(max_length = 100)
	lname     = models.CharField(max_length = 100)
	org       = models.CharField(max_length = 100)
	orgtype   = models.CharField(max_length = 100)
	username  = models.CharField(max_length = 100)
	password  = models.CharField(max_length = 100)
	machineid = models.CharField(max_length = 10)
	lastLogin = models.DateTimeField(null = True, blank = True)

class Machine(models.Model):
	machineid = models.CharField(max_length = 10)
	ON = 'ON'
	OFF = 'OFF'
	MAINTENANCE = "MN"
	MACHINE_STATUS_CHOICES = (
        (ON, 'On'),
        (OFF, 'Off'),
        (MAINTENANCE, 'MAINTENANCE'),        
    )
	machine_status = models.CharField(
        max_length=3,
        choices=MACHINE_STATUS_CHOICES,
        default=OFF,
    )
	ambient_temp = models.IntegerField()
	water_temp = models.IntegerField()
	set_temp = models.IntegerField()
	temp_set_by = models.CharField(max_length = 20, null = True, blank = True)
