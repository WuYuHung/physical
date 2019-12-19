from django.shortcuts import render, redirect


def index(request):
    if request.user.is_authenticated and request.user.has_perm("doctor.doctor"):
        return render(request, "doctor.html", {})
    else:
        return redirect("/patient/")
