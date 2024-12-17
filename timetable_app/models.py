from django.db import models

# Create your models here.

from django.db import models

class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name

class Lecturer(models.Model):
    lecturer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=200)
    credits = models.IntegerField()
    year_level = models.IntegerField()

    def __str__(self):
        return self.course_name
class Schedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    day = models.CharField(max_length=20)
    time_slot = models.CharField(max_length=50)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.course.course_name} - {self.day} {self.time_slot}"
