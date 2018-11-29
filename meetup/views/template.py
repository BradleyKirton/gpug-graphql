from django.views import View
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect


import meetup.models


class Task(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        """Render the tasks page."""

        meetups = meetup.models.Meetup.objects.all()
        context = {
            "django_context": {"meetups": meetups},
            "vue_context": {"meetups": list(meetups.values())},
        }

        return render(request, "meetup/tasks.html", context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        name = request.POST["name"]

        if name is None:
            return redirect("tasks-page")

        meetup.tasks.sync_meetup.send(name)
        return redirect("tasks-page")
