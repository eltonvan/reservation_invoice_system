from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect


class CustomLoginRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user.id != request.user.id:
            template_name = "invoice/404.html"
            return render(request, template_name, status=404)
            # if request.user.id != kwargs["pk"]:
            #     return redirect("authorized")
        return super().dispatch(request, *args, **kwargs)


class CustomAuthorizationMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
