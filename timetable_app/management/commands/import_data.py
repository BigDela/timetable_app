import pandas as pd
from django.core.management.base import BaseCommand
from timetable_app.models import Room, Course, Lecturer  # Import your models

class Command(BaseCommand):
    help = 'Import data into Room, Course, or Lecturer models from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('model', type=str, help='Model to import data into (room, course, lecturer)')
        parser.add_argument('file_path', type=str, help='Path to the Excel file')

    def handle(self, *args, **kwargs):
        model = kwargs['model'].lower()
        file_path = kwargs['file_path']

        try:
            # Load the Excel file
            data = pd.read_excel(file_path)

            if model == 'room':
                self.import_rooms(data)
            elif model == 'course':
                self.import_courses(data)
            elif model == 'lecturer':
                self.import_lecturers(data)
            else:
                self.stdout.write(self.style.ERROR(f"Invalid model: {model}. Choose from 'room', 'course', or 'lecturer'."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))

    def import_rooms(self, data):
        for _, row in data.iterrows():
            Room.objects.get_or_create(
                name=row['name'],
                defaults={'capacity': row['capacity']}
            )
        self.stdout.write(self.style.SUCCESS('Successfully imported Room data!'))

    def import_courses(self, data):
        for _, row in data.iterrows():
            Course.objects.get_or_create(
                course_name=row['course_name'],
                defaults={
                    'credits': row['credits'],
                    'year_level': row['year_level']
                }
            )
        self.stdout.write(self.style.SUCCESS('Successfully imported Course data!'))

    def import_lecturers(self, data):
        for _, row in data.iterrows():
            Lecturer.objects.get_or_create(
                name=row['name'],
                defaults={'department': row['department']}
            )
        self.stdout.write(self.style.SUCCESS('Successfully imported Lecturer data!'))
