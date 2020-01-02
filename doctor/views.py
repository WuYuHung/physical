from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from doctor.forms import HomeForm
from datetime import datetime
from django.contrib.auth.models import User, Permission
import json
from patient.models import Task
from django.utils import timezone

# def index(request):
#     if request.user.is_authenticated and request.user.has_perm("doctor.doctor"):
#         return render(request, "doctor.html", {})
#     else:
#         return redirect("/patient/")


class HomeView(TemplateView):
    template_name = "doctor.html"

    def get(self, request):
        form = HomeForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        username = None
        if request.user.is_authenticated:
            username = request.user.username
        form = HomeForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            kinds = json.loads(instance.kind.replace("'", '"'))
            print(datetime.now())
            for kind in kinds:
                instance.kind = kind
                Task.objects.create(
                    patient=instance.patient,
                    kind=kind,
                    doctor=username,
                    start_time=timezone.now(),
                )
            user = User.objects.create_user(
                username=instance.patient, password=instance.patient
            )
            perm = Permission.objects.get(name="patient")
            user.user_permissions.add(perm)
            #   text = form.cleaned_data['post']
            form = HomeForm()
            return redirect("/doctor")  # Add
        return render(request, self.template_name, {"form": form})

