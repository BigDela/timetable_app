from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Schedule, Room, Course, Lecturer
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test


def is_admin(user):
    return user.groups.filter(name__in=['Admin']).exists() or user.is_superuser

@user_passes_test(is_admin , login_url='/not_authorized/')
@login_required
def create_schedule(request):
    if request.method == 'POST':
        # Fetch form data
        day = request.POST.get('day')
        time_slot = request.POST.get('time_slot')
        room_id = request.POST.get('room')
        course_id = request.POST.get('course')
        lecturer_id = request.POST.get('lecturer')

        # Debugging: Print submitted data
        print(f"Day: {day}")
        print(f"Time Slot: {time_slot}")
        print(f"Room ID: {room_id}")
        print(f"Course ID: {course_id}")
        print(f"Lecturer ID: {lecturer_id}")

        # Validate all fields
        if not (day and time_slot and room_id and course_id and lecturer_id):
            messages.error(request, "All fields are required. Please fill out the form completely.")
            return redirect('create_schedule')

        try:
            # Fetch foreign key objects
            room = Room.objects.get(room_id=room_id)
            course = Course.objects.get(course_id=course_id)
            lecturer = Lecturer.objects.get(lecturer_id=lecturer_id)

            # Check for conflicts
            conflict = Schedule.objects.filter(day=day, time_slot=time_slot, room=room) | \
                       Schedule.objects.filter(day=day, time_slot=time_slot, lecturer=lecturer)

            if conflict.exists():
                messages.error(request, "Scheduling conflict detected. Please choose a different time or room.")
                return redirect('create_schedule')

            # Save the schedule
            Schedule.objects.create(day=day, time_slot=time_slot, room=room, course=course, lecturer=lecturer)
            messages.success(request, "Schedule created successfully!")
            return redirect('create_schedule')

        except Room.DoesNotExist:
            messages.error(request, "The selected room does not exist.")
        except Course.DoesNotExist:
            messages.error(request, "The selected course does not exist.")
        except Lecturer.DoesNotExist:
            messages.error(request, "The selected lecturer does not exist.")

    # Fetch data for dropdowns
    rooms = Room.objects.all()
    courses = Course.objects.all()
    lecturers = Lecturer.objects.all()

    return render(request, 'timetable_app/create_schedule.html', {
        'rooms': rooms,
        'courses': courses,
        'lecturers': lecturers,
    })
from django.shortcuts import render
from .models import Schedule

def schedule_list(request):
    # Fetch all schedules with their related room, course, and lecturer data
    schedules = Schedule.objects.select_related('room', 'course', 'lecturer').all()

    # Render the schedule list template and pass the schedules to it
    return render(request, 'timetable_app/schedule_list.html', {'schedules': schedules})

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import Schedule, Room, Course, Lecturer

@user_passes_test(is_admin , login_url='/not_authorized/')
@login_required
def edit_schedule(request, schedule_id):
    # Fetch the schedule object or return 404 if not found
    schedule = get_object_or_404(Schedule, schedule_id=schedule_id)
    print(f"POST data: {request.POST}")


    if request.method == 'POST':
        # Update the schedule with form data
        day = request.POST.get('day')
        time_slot = request.POST.get('time_slot')
        room_id = request.POST.get('room')
        course_id = request.POST.get('course')
        lecturer_id = request.POST.get('lecturer')

        try:
            room = Room.objects.get(room_id=room_id)
            course = Course.objects.get(course_id=course_id)
            lecturer = Lecturer.objects.get(lecturer_id=lecturer_id)

            # Update the schedule object
            schedule.day = day
            schedule.time_slot = time_slot
            schedule.room = room
            schedule.course = course
            schedule.lecturer = lecturer
            schedule.save()

            messages.success(request, "Schedule updated successfully!")
            return redirect('schedule_list')

        except Room.DoesNotExist:
            messages.error(request, "The selected room does not exist.")
        except Course.DoesNotExist:
            messages.error(request, "The selected course does not exist.")
        except Lecturer.DoesNotExist:
            messages.error(request, "The selected lecturer does not exist.")

    # Fetch dropdown data for the form
    rooms = Room.objects.all()
    courses = Course.objects.all()
    lecturers = Lecturer.objects.all()

    return render(request, 'timetable_app/edit_schedule.html', {
        'schedule': schedule,
        'rooms': rooms,
        'courses': courses,
        'lecturers': lecturers,
    })

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Schedule

@user_passes_test(is_admin , login_url='/not_authorized/')
@login_required
def clear_schedule(request, schedule_id):
    # Get the schedule object to be deleted
    schedule = get_object_or_404(Schedule, schedule_id=schedule_id)

    # Delete the schedule
    schedule.delete()

    # Add a success message
    messages.success(request, "Schedule deleted successfully!")

    # Redirect back to the schedule list
    return redirect('schedule_list')

from django.contrib.auth import login
from django.shortcuts import redirect, render

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect based on user role
            if user.is_superuser:
                return redirect('/admin_dashboard/')
            elif user.groups.filter(name='Lecturer').exists():
                return redirect('/lecturer_dashboard/')
            else:
                return redirect('/schedule_list/')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'login.html')

from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout(request):
    logout(request)
    print("User has been logged out")  # Debugging logout
    return redirect('login')

from django.shortcuts import render

def not_authorized(request):
    return render(request, 'timetable_app/not_authorized.html')

@login_required  # Ensures only logged-in users can access the homepage
def homepage(request):
    return render(request, 'timetable_app/homepage.html')
