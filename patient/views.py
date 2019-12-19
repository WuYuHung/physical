from django.shortcuts import render
import plotly.figure_factory as ff


def index(request):

    df = [
        dict(
            Task="Morning Sleep",
            Start="2016-01-01",
            Finish="2016-01-01 6:00:00",
            Resource="Sleep",
        ),
        dict(
            Task="Breakfast",
            Start="2016-01-01 7:00:00",
            Finish="2016-01-01 7:30:00",
            Resource="Food",
        ),
        dict(
            Task="Work",
            Start="2016-01-01 9:00:00",
            Finish="2016-01-01 11:25:00",
            Resource="Brain",
        ),
        dict(
            Task="Break",
            Start="2016-01-01 11:30:00",
            Finish="2016-01-01 12:00:00",
            Resource="Rest",
        ),
        dict(
            Task="Lunch",
            Start="2016-01-01 12:00:00",
            Finish="2016-01-01 13:00:00",
            Resource="Food",
        ),
        dict(
            Task="Work",
            Start="2016-01-01 13:00:00",
            Finish="2016-01-01 17:00:00",
            Resource="Brain",
        ),
        dict(
            Task="Exercise",
            Start="2016-01-01 17:30:00",
            Finish="2016-01-01 18:30:00",
            Resource="Cardio",
        ),
        dict(
            Task="Post Workout Rest",
            Start="2016-01-01 18:30:00",
            Finish="2016-01-01 19:00:00",
            Resource="Rest",
        ),
        dict(
            Task="Dinner",
            Start="2016-01-01 19:00:00",
            Finish="2016-01-01 20:00:00",
            Resource="Food",
        ),
        dict(
            Task="Evening Sleep",
            Start="2016-01-01 21:00:00",
            Finish="2016-01-01 23:59:00",
            Resource="Sleep",
        ),
    ]
    fig = ff.create_gantt(df)
    string = fig.to_html()

    return render(request, "patient.html", {"chart": string})
