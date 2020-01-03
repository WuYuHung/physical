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
from datetime import datetime
import math
from django.http import HttpResponseForbidden


# def index(request):
#     if request.user.is_authenticated and request.user.has_perm("doctor.doctor"):
#         return render(request, "doctor.html", {})
#     else:
#         return redirect("/patient/")

kind_dict = {i: index for index, i in enumerate(("抽血", "心電圖", "X光", "視力檢查", "聽力檢查"))}


def get_base():
    tasks = Task.objects.all()
    time_stamp = math.inf
    if not tasks:
        return datetime.fromtimestamp((datetime.now().timestamp() // 300) * 300)
    for task in tasks:
        current = task.start_time.timestamp()
        if task.start_time.timestamp() < time_stamp:
            time_stamp = current
    return datetime.fromtimestamp((current // 300) * 300)


def get_table():
    base = get_base()
    time_table = [list() for i in range(999)]
    tasks = Task.objects.all()
    for task in tasks:
        now_time = task.start_time
        now_index = int((now_time - base).total_seconds() // 300)
        time_table[now_index].append(kind_dict[task.kind])
    return time_table


class HomeView(TemplateView):
    template_name = "doctor.html"

    def get(self, request):
        if not (
            request.user.is_authenticated and request.user.has_perm("doctor.doctor")
        ):
            return HttpResponseForbidden("403 Forbidden", content_type="text/html")
        form = HomeForm()
        username = None
        if request.user.is_authenticated:
            username = request.user.username
        tasks = Task.objects.all()
        df = list()
        if not tasks:
            return render(
                request,
                self.template_name,
                {"form": form, "chart": "", "username": username},
            )
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
            title="健康檢查時程表",
            show_hover_fill=False,
        )
        string = fig.to_html()
        return render(
            request,
            self.template_name,
            {"form": form, "chart": string, "username": username},
        )

    def post(self, request):
        username = None
        if request.user.is_authenticated:
            username = request.user.username
        form = HomeForm(request.POST)
        if form.is_valid():
            base = get_base()
            instance = form.save(commit=False)
            kinds = json.loads(instance.kind.replace("'", '"'))
            task_todo = list()
            for i in kinds:
                task_todo.append(kind_dict[i])

            now_time = datetime.fromtimestamp(
                ((int(datetime.now().timestamp()) + 300) // 300 + 1) * 300
            )
            now_index = int((now_time - base).total_seconds() // 300)
            iterator = now_index
            location = [None] * 5
            time = get_table()
            while True:
                flag = 0
                for i in task_todo:
                    if i not in time[iterator]:
                        time[iterator].append(i)
                        location[i] = iterator
                        iterator += 2
                        flag = 1
                        task_todo.remove(i)
                        break
                if len(task_todo) == 0:
                    break
                if flag != 1:
                    iterator += 1

            for index, kind in enumerate(kinds):
                Task.objects.create(
                    patient=instance.patient,
                    kind=kind,
                    doctor=username,
                    start_time=base + timedelta(minutes=5 * location[kind_dict[kind]]),
                )
            user = User.objects.create_user(
                username=instance.patient, password=instance.patient
            )
            perm = Permission.objects.get(name="patient")
            user.user_permissions.add(perm)
            #   text = form.cleaned_data['post']
            form = HomeForm()
            return redirect("/doctor")  # Add
        return render(request, self.template_name, {"form": form, "username": username})
