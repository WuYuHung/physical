from django.shortcuts import render
import plotly.figure_factory as ff


def index(request):
    df = [
        dict(
            Task="華國瑜",
            Start="2016-01-01 6:00:00",
            Finish="2016-01-01 6:00:02",
            Resource="Sleep",
        ),
        dict(
            Task="華國瑜",
            Start="2016-01-01 6:00:04",
            Finish="2016-01-01 6:00:06",
            Resource="Sleep",
        ),
    ]
    fig = ff.create_gantt(
        df, index_col="Resource", show_colorbar=True, group_tasks=True
    )
    string = fig.to_html()

    return render(request, "patient.html", {"chart": string})
