from django.shortcuts import render
from django.http import HttpResponse
import plotly.figure_factory as ff
from .models import Task
from datetime import timedelta


def index(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    tasks = Task.objects.filter(patient=username)
    df = list()
    for task in tasks:
        temp_dict = dict(Task=task.kind)
        temp_dict["Task"] = task.kind
        dt = task.start_time
        temp_dict["Start"] = dt.strftime("%Y-%m-%d %H:%M:%S")
        temp_dict["Finish"] = (dt + timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
        temp_dict["Resource"] = task.kind
        df.append(temp_dict)
    fig = ff.create_gantt(
        df, index_col="Resource", show_colorbar=True, group_tasks=True
    )
    string = fig.to_html()

    return render(request, "patient.html", {"chart": string, "username": username})

