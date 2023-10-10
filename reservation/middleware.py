from typing import Any
from django.http import Http404
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin


class CustomDetailViewMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self,request):
        response = self.get_response(request)
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        if isinstance(view_func, DetailView) and not isinstance(view_func, LoginRequiredMixin):

            obj = view_kwargs.get('object')
            if obj and hasattr(obj, 'user') and obj.user_id != request.user.id:
                raise Http404("You are not authorized")
        return None
    