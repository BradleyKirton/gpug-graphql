import django.views
import django.shortcuts
import django.http
import rest_framework.viewsets
import meetup.tasks
import meetup.models
import meetup.serializers


class MeetupViewSet(rest_framework.viewsets.ModelViewSet):
	queryset = meetup.models.Meetup.objects.all()
	serializer_class = meetup.serializers.MeetupSerializer


class EventViewSet(rest_framework.viewsets.ModelViewSet):
	queryset = meetup.models.Event.objects.all()
	serializer_class = meetup.serializers.EventSerializer


class AttendeeViewSet(rest_framework.viewsets.ModelViewSet):
	queryset = meetup.models.Attendee.objects.all()
	serializer_class = meetup.serializers.AttendeeSerializer


class AttendanceViewSet(rest_framework.viewsets.ModelViewSet):
	queryset = meetup.models.Attendance.objects.all()
	serializer_class = meetup.serializers.AttendanceSerializer


# DRF Integrated GraphQL view
import graphene
import graphene_django.views

from rest_framework.settings import api_settings
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.decorators import authentication_classes
from django.http import HttpRequest
from rest_framework.request import Request
from typing import Any, Union


class RestGraphQL(graphene_django.views.GraphQLView):
	"""A sub class of the django graphene GraphQLView which integrates with
	the useful authentication, permission and api_view functionality of the DRF.
	"""
	def parse_body(self, request: Union[HttpRequest, Request]) -> Any:
		if isinstance(request, Request):
			return request.data

		return super().parse_body(request)

	@classmethod
	def as_view(cls: 'RestGraphQL', schema: graphene.Schema) -> 'RestGraphQL':
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
		return api_view(http_method_names=('GET', 'POST'))(view)


class Task(django.views.View):
	def get(self, request: django.http.HttpRequest) -> django.http.HttpResponse:
		meetups = meetup.models.Meetup.objects.all()
		return django.shortcuts.render(
			request, 
			'meetup/tasks.html', 
			{'meetups': meetups}
		)

	def post(self, request: django.http.HttpRequest) -> django.http.HttpResponse:
		name = request.POST['name']
		
		if name is None:
			return django.shortcuts.redirect('tasks-page')

		meetup.tasks.sync_meetup.send(name)
		return django.shortcuts.redirect('tasks-page')