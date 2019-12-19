from django.contrib import auth
from django.shortcuts import render, redirect


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")
    user = auth.authenticate(username=username, password=password)
    error_msg = str()
    if user:
        print(user.password)
        auth.login(request, user)
        if user.has_perm("patient.patient"):
            return redirect(request.GET.get("next", "/patient"))
        return redirect(request.GET.get("next", "/"))
    else:
        error_msg = "帳號或密碼錯誤！"
    return render(request, "login.html", {"error_msg": error_msg})
