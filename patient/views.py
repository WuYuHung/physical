from django.shortcuts import render
from django.http import HttpResponse
import plotly.figure_factory as ff



def index(request):
    df = [
        dict(
            Task="華國瑜",
            Start="2016-01-01 6:00:00",
            Finish="2016-01-01 6:08:00",
            Resource="Blood test",
        ), 
        dict(
            Task="華國瑜",
            Start="2016-01-01 6:10:00",
            Finish="2016-01-01 6:20:00",
            Resource="Vision test",
        ),
        dict(
            Task="華國瑜",
            Start="2016-01-01 6:22:00",
            Finish="2016-01-01 6:30:00",
            Resource="Hearing test",
        ),
        dict(
            Task="華國瑜",
            Start="2016-01-01 6:32:00",
            Finish="2016-01-01 6:38:00",
            Resource="X-ray test",
        ),
        dict(
            Task="華國瑜",
            Start="2016-01-01 6:40:00",
            Finish="2016-01-01 6:50:00",
            Resource="Urine routine",
        ),
        dict(
            Task="俞國華",
            Start="2016-01-01 6:08:00",
            Finish="2016-01-01 6:16:00",
            Resource="Blood test",
        ), 
        dict(
            Task="俞國華",
            Start="2016-01-01 6:20:00",
            Finish="2016-01-01 6:30:00",
            Resource="Vision test",
        ),
        dict(
            Task="俞國華",
            Start="2016-01-01 6:32:00",
            Finish="2016-01-01 6:40:00",
            Resource="Hearing test",
        ),
        dict(
            Task="俞國華",
            Start="2016-01-01 6:42:00",
            Finish="2016-01-01 6:50:00",
            Resource="X-ray test",
        ),
        dict(
            Task="俞國華",
            Start="2016-01-01 6:52:00",
            Finish="2016-01-01 7:02:00",
            Resource="Urine routine",
        ),
    ]
    fig = ff.create_gantt(
        df, index_col="Resource", show_colorbar=True, group_tasks=True
    )
    string = fig.to_html()

    return render(request, "patient.html", {"chart": string})

