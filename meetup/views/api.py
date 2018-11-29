from typing import Any, Union
from rest_framework.settings import api_settings
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.decorators import authentication_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import serializers
from django.http import HttpRequest
from meetup import tasks
from meetup.models import Meetup, Event, Attendee, Attendance
from meetup.serializers import (
    MeetupSerializer,
    EventSerializer,
    AttendeeSerializer,
    AttendanceSerializer,
    SyncMeetupPayloadSerializer,
)

import graphene
import graphene_django.views


@api_view(["POST"])
def sync_meetup(request: Request) -> Response:
    """Sync an individual meetup."""

    serializer = SyncMeetupPayloadSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        meetup_id = serializer.validated_data.get("meetup_id", None)
        meetup = Meetup.objects.get(pk=meetup_id)
    except Meetup.DoesNotExist:
        raise serializers.ValidationError(
            {"non_field_errors": [f"invalid meetup_id '{meetup_id}'"]}
        )

    tasks.sync_meetup.send(name=meetup.name)
    serializer = MeetupSerializer(instance=meetup)
    return Response(serializer.data)


class MeetupViewSet(viewsets.ModelViewSet):
    queryset = Meetup.objects.all()
    serializer_class = MeetupSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class AttendeeViewSet(viewsets.ModelViewSet):
    queryset = Attendee.objects.all()
    serializer_class = AttendeeSerializer


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer


class RestGraphQL(graphene_django.views.GraphQLView):
    """A sub class of the django graphene GraphQLView which integrates with
    the useful authentication, permission and api_view functionality of the DRF.
    """

    def parse_body(self, request: Union[HttpRequest, Request]) -> Any:
        if isinstance(request, Request):
            return request.data

        return super().parse_body(request)

    @classmethod
    def as_view(cls: "RestGraphQL", schema: graphene.Schema) -> "RestGraphQL":
        """Instantiate the RestGraphQL instance and wrap the view with the DRF
        authentication_classes, permission_classes and api_view decorators.

        Args:
            cls (RestGraphQL): The RestGraphQL class object
            schema (Schema): A graphene Schema object
        
        Returns:
            A django view
        """
        view = super().as_view(graphiql=True, schema=schema)
        view = authentication_classes(api_settings.DEFAULT_AUTHENTICATION_CLASSES)(view)
        view = permission_classes(api_settings.DEFAULT_PERMISSION_CLASSES)(view)
        return api_view(http_method_names=("GET", "POST"))(view)
