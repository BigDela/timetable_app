# Generated by Django 5.1.4 on 2024-12-14 11:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.AutoField(primary_key=True, serialize=False)),
                ('course_name', models.CharField(max_length=200)),
                ('credits', models.IntegerField()),
                ('year_level', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Lecturer',
            fields=[
                ('lecturer_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('department', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('room_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('capacity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('schedule_id', models.AutoField(primary_key=True, serialize=False)),
                ('day', models.CharField(max_length=20)),
                ('time_slot', models.CharField(max_length=50)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable_app.course')),
                ('lecturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable_app.lecturer')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable_app.room')),
            ],
        ),
    ]
