from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from doctor.forms import HomeForm
from datetime import datetime
from django.contrib.auth.models import User, Permission
import json
from patient.models import Task
from django.utils import timezone
from django.http import HttpResponse
import plotly.figure_factory as ff
from patient.models import Task
from datetime import timedelta

# def index(request):
#     if request.user.is_authenticated and request.user.has_perm("doctor.doctor"):
#         return render(request, "doctor.html", {})
#     else:
#         return redirect("/patient/")
time = list(list() * 20)


class HomeView(TemplateView):
    template_name = "doctor.html"

    def get(self, request):
        form = HomeForm()
        username = None
        if request.user.is_authenticated:
            username = request.user.username
        tasks = Task.objects.all()
        print(request.user.username)
        df = list()
        for task in tasks:
            temp_dict = dict(Task=task.kind)
            temp_dict["Task"] = task.patient
            dt = task.start_time
            temp_dict["Start"] = dt.strftime("%Y-%m-%d %H:%M:%S")
            temp_dict["Finish"] = (dt + timedelta(minutes=5)).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            temp_dict["Resource"] = task.kind
            df.append(temp_dict)
        fig = ff.create_gantt(
            df,
            index_col="Resource",
            show_colorbar=True,
            group_tasks=True,
            title=username + "健康檢查時程表",
            show_hover_fill=False,
        )
        string = fig.to_html()
        return render(
            request,
            self.template_name,
            {"form": form, "chart": string, "user": username},
        )

    def post(self, request):
        username = None
        if request.user.is_authenticated:
            username = request.user.username
        form = HomeForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            kinds = json.loads(instance.kind.replace("'", '"'))
            print(datetime.now())
            for index, kind in enumerate(kinds):
                instance.kind = kind
                Task.objects.create(
                    patient=instance.patient,
                    kind=kind,
                    doctor=username,
                    start_time=timezone.now() + timedelta(minutes=5 * index),
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
