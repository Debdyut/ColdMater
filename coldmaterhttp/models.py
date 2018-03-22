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
