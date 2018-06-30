import graphene
import graphene_django

from typing import Dict, Any
from django.db.models.query import QuerySet
from meetup.models import Meetup
from meetup.models import Event
from meetup.models import Attendee
from meetup.models import Attendance


class MeetupType(graphene_django.DjangoObjectType):
	"""GraphQL type for Meetup model"""
	class Meta:
		model = Meetup


class EventType(graphene_django.DjangoObjectType):
	"""GraphQL type for Event model"""
	class Meta:
		model = Event


class AttendeeType(graphene_django.DjangoObjectType):
	"""GraphQL type for Attendee model"""
	class Meta:
		model = Attendee


class AttendanceType(graphene_django.DjangoObjectType):
	"""GraphQL type for Attendance model"""
	class Meta:
		model = Attendance


class MeetupQuery:
	"""Query which provides access to all meetups."""
	meetup = graphene.Field(
		MeetupType, 
		id=graphene.Int(),
		name=graphene.String(),
		description="Fetch a specific meetup by specifying the 'id' or 'name'."
	)
	
	all_meetups = graphene.List(
		MeetupType,
		limit=graphene.Int(),
		description="All meetups available in the application."
	)

	def resolve_meetup(self, info: Any, **kwargs: Dict) -> Meetup:
		"""

		Args:
		   info (Any):

		Returns:
		    A Meetup instance
		"""
		pk = kwargs.get('id', None)
		name = kwargs.get('name', None)

		if pk is not None:
			return Meetup.objects.get(pk=pk)

		if name is not None:
			return Meetup.objects.get(name=name)

	def resolve_all_meetups(self, info: Any, **kwargs: Dict) -> QuerySet:
		"""Return a list of all meetups. Optionally limit the records if the
		client provides a `limit` input.

		Args:
		   info (Any):

		Returns:
		    A Meetup queryset
		"""
		limit = kwargs.get('limit', None)
		meetups = Meetup.objects.all()

		if limit is None:
			return meetups

		return meetups[:limit]

class EventQuery:
	event = graphene.Field(
		EventType, 
		id=graphene.Int(),
		name=graphene.String()
	)

	all_events = graphene.List(
		EventType,
		limit=graphene.Int()
	)

	def resolve_event(self, info: Any, **kwargs: Dict) -> Event:
		"""

		Args:
		   info (Any):

		Returns:
		    A Event instance
		"""
		pk = kwargs.get('id', None)
		name = kwargs.get('name', None)

		if pk is not None:
			return Event.objects.get(pk=pk)

		if name is not None:
			return Event.objects.get(name=name)

	def resolve_all_events(self, info: Any, **kwargs: Dict) -> QuerySet:
		"""

		Args:
		   info (Any):

		Returns:
		    A Event queryset
		"""
		limit = kwargs.get('limit', None)
		events = Event.objects.all()
		
		if limit is None:
			return events
		
		return events[:limit]

class AttendeeQuery:
	attendee = graphene.Field(
		AttendeeType, 
		id=graphene.Int(),
		name=graphene.String()
	)
	all_attendees = graphene.List(AttendeeType)

	def resolve_attendee(self, info: Any, **kwargs: Dict) -> Attendee:
		"""

		Args:
		   info (Any):

		Returns:
		    An Attendee instance
		"""
		pk = kwargs.get('id', None)
		name = kwargs.get('name', None)

		if pk is not None:
			return Attendee.objects.get(pk=pk)

		if name is not None:
			return Attendee.objects.get(name=name)

	def resolve_all_attendees(self, info: Any, **kwargs: Dict) -> QuerySet:
		"""

		Args:
		   info (Any):

		Returns:
		    An Attendee queryset
		"""
		return Attendee.objects.all()


class AttendanceQuery:
	attendance = graphene.Field(AttendanceType, id=graphene.Int())
	all_attendances = graphene.List(AttendanceType)

	def resolve_attendance(self, info: Any, **kwargs: Dict) -> Attendance:
		"""

		Args:
		   info (Any):

		Returns:
		    An Attendance instance
		"""
		pk = kwargs.get('id', None)
		
		if pk is None:
			return

		return Attendance.objects.get(pk=pk)

	def resolve_all_attendances(self, info: Any, **kwargs: Dict) -> QuerySet:
		"""

		Args:
		   info (Any):

		Returns:
		    An Attendance queryset
		"""
		return Attendance.objects.all()


class Query(
	MeetupQuery,
	EventQuery,
	AttendeeQuery,
	AttendanceQuery,
	graphene.ObjectType
):
	"""
	# Root Query
	### Root query for the application.
	
	This documentation comes directly from the doc string
	for the `meetup.schema:Query class`. The doc string contains
	markdown.

	The root query of the application provides the access to the following:

		- MeetupQuery
		- EventQuery
		- AttendeeQuery
		- AttendanceQuery
	"""
	pass

