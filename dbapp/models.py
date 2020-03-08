from django.db import models


class Department(models.Model):
    department = models.CharField(max_length=40, primary_key=True)
    description = models.CharField(max_length=2000)


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    problem_statement = models.CharField(max_length=1000)
    event_date = models.DateTimeField()
    people_required = models.IntegerField()
    fees = models.IntegerField()
    rules = models.CharField(max_length=10000)
    img = models.ImageField(upload_to='img')


class Participant(models.Model):
    participant_id = models.AutoField(primary_key=True)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    birthdate = models.DateField()
    gender = models.CharField(max_length=7)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    college_name = models.CharField(max_length=100)
    mobile = models.IntegerField()
    email = models.CharField(max_length=100)
