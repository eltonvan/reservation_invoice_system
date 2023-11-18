from home.models import CustomUser
from reservation.models import Reservation
from django.http import HttpResponseForbidden
from django.shortcuts import redirect 
from django.urls import resolve


class CustomUserAuthPermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_reservations = Reservation.objects.filter(user_id=request.user.id)
        allowed_pk = [item.id for item in allowed_reservations]
        primary_key = resolve(request.path).kwargs.get('pk')
        if primary_key not in allowed_pk:
            return HttpResponseForbidden("you are not authorized to view this page")

        response = self.get_response(request)
        return response
