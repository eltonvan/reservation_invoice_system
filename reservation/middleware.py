from typing import Any
from django.http import Http404
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import CustomLoginRequiredMixin

class CustomDetailViewMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        print("middleware called")
        print(request.user.id)

        view_class = view_func.__class__
        model = getattr(view_class, 'model', None)
        pk = view_kwargs.get('pk')
        print(model, pk)
            

        if isinstance(view_func, DetailView):
            view_class = view_func.__class__
            model = getattr(view_class, 'model', None)
            pk = view_kwargs.get('pk')
            

            if model and pk:
                try:
                    obj = model.objects.get(pk=pk)
                    print(obj)
                    if obj is not None and hasattr(obj, 'user') and obj.user.id != request.user.id:
                        print("userid:", request.user.id)
                        raise Http404("You are not authorized")
                except model.DoesNotExist:
                    raise Http404("Object not found")

        return None
