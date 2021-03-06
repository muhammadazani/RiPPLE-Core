# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from json import loads
from users.models import CourseUser

from django.http import JsonResponse, HttpResponse

from users.services import UserService
from recommendations.services import AvailabilityService

def user_availability(request):
    logged_in_user = UserService.logged_in_user(request)
    availability = [x.toJSON() for x in AvailabilityService.get_user_availability(logged_in_user)]
    return JsonResponse({"data": availability})

def course_availability(request):
    course = UserService.logged_in_user(request).course
    counts = AvailabilityService.get_course_availability(course)

    # Get the count of each user in the course
    return JsonResponse({"data": counts})

def days(request):
    days = [x.toJSON() for x in AvailabilityService.get_days()]
    return JsonResponse({"data": days })

def update_availability(request):
    # HTTP.POST is required for this.
    if request.method != "POST":
        return JsonResponse({
            "error": "Must use POST to this endpoint"
        }, status=405)

    logged_in_user = UserService.logged_in_user(request)

    post_request = loads(request.body.decode("utf-8"))
    day = post_request.get("day", None)
    time = post_request.get("time", None)
    updated_availability = AvailabilityService.update_availability(logged_in_user, day, time)
    if updated_availability is None:
        return JsonResponse({"error": "Invalid day/time/availability combination"}, status=422)
    else:
        return JsonResponse({"data": updated_availability.toJSON()})

def utc_times(request):
    times = [x.toJSON() for x in AvailabilityService.get_utc_times()]
    return JsonResponse({"data": times})

def study_roles(request):
    roles = [x.toJSON() for x in AvailabilityService.get_study_roles()]
    return JsonResponse({"data": roles})

def user_roles(request):
    logged_in_user = UserService.logged_in_user(request)
    available_roles = [x.toJSON() for x in AvailabilityService.get_user_available_roles(logged_in_user)]
    return JsonResponse({"data": available_roles})

def update_role(request):
    # HTTP.POST is required for this.
    if request.method != "POST":
        return JsonResponse({
            "error": "Must use POST to this endpoint"
        }, status=405)

    logged_in_user = UserService.logged_in_user(request)

    post_request = loads(request.body.decode("utf-8"))
    topic = post_request.get("topic", None)
    study_role = post_request.get("studyRole", None)

    updated_role = AvailabilityService.update_role(logged_in_user, topic, study_role)

    if updated_role is None:
        return JsonResponse({"error": "Invalid topic/studyRole/availableRole combination"}, status=422)
    else:
        return JsonResponse(updated_role.toJSON())
