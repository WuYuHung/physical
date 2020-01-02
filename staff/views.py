from django.shortcuts import render, redirect
from patient.models import Task
from datetime import timedelta
import plotly.figure_factory as ff
from django.contrib.auth.models import Permission, User
from django.http import HttpResponseForbidden

KINDS = {"blood": "抽血", "heart": "心電圖", "x-ray": "X光", "sight": "視力檢查", "hear": "聽力檢查"}


def get_user_permissions(user):
    if user.is_superuser:
        return Permission.objects.all()
    return user.user_permissions.all() | Permission.objects.filter(group__user=user)


def index(request):
    if not (
        request.user.is_authenticated
        and (
            request.user.has_perm("staff.blood")
            or request.user.has_perm("staff.x-ray")
            or request.user.has_perm("staff.heart")
            or request.user.has_perm("staff.sight")
            or request.user.has_perm("staff.hear")
        )
    ):
        return HttpResponseForbidden("403 Forbidden", content_type="text/html")
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    perm = get_user_permissions(request.user)[0].codename
    kind = KINDS[perm]
    tasks = Task.objects.filter(kind=kind)
    df = list()
    charts = list()
    for task in tasks:
        temp_dict = dict(Task=task.patient, Resource=kind)
        dt = task.start_time
        temp_dict["Start"] = dt.strftime("%Y-%m-%d %H:%M:%S")
        temp_dict["Finish"] = (dt + timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
        df.append(temp_dict)
    fig = ff.create_gantt(
        df,
        index_col="Resource",
        show_colorbar=True,
        group_tasks=True,
        title=kind + "健康檢查時程表",
        show_hover_fill=False,
    )
    string = fig.to_html()
    return render(request, "staff.html", {"chart": string, "department": kind})
