from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

class CustomLoginRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):

        if self.get_object().user.id != request.user.id:
            template_name = 'invoice/404.html'
            return render(request, template_name, status=404)
        return super().dispatch(request, *args, **kwargs)
