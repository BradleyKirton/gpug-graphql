import os
import dramatiq
import requests
import meetup.models
import meetup.exceptions

from django.conf import settings
from typing import List, Dict, Optional


def get_api_key() -> Optional[str]:
	"""Fetches the api key from the environment variables.

	Note if the key has not been set the function returns None.

	Returns:
	    A meetup api key
	"""
	try:
		return os.environ[settings.MEETUP_API_ENV_NAME]
	except:
		return

# Gauteng-Python-Users-Group
@dramatiq.actor
def sync_all_meetups() -> None:
	"""Fetches the past events for each of the meetup's in the Meetup table."""
	api_key =  get_api_key()
	
	if api_key is None:
		raise meetup.exceptions.MissingApiKey('API not set in environment variables')

	queryset = meetup.models.Meetup.objects.all()
	for meetup_instance in queryset:
		sync_meetup(meetup_instance.name)


@dramatiq.actor
def sync_meetup(name: str) -> None:
	"""Fetches the past events for each of the meetup's in the Meetup table."""
	api_key =  get_api_key()
	
	if api_key is None:
		raise meetup.exceptions.MissingApiKey('API not set in environment variables')

	queryset = meetup.models.Meetup.objects.filter(syncing=False)

	for meetup_instance in queryset:
		meetup_instance.syncing = True
		meetup_instance.save()

		events = fetch_events(meetup_instance.name, api_key)

		for event in events:
			defaults = event.copy()
			event_id = defaults.pop('event_id')
			
			# Create an event instance
			event_instance, created = meetup.models.Event.objects.get_or_create(
				event_id=event_id,
				meetup_id=meetup_instance.pk,
				defaults=defaults
			)

			# If the record already exists continue the loop
			if created:
				continue

			attendance = fetch_attendance(meetup_instance.name, event_instance.event_id, api_key)
			for attendee in attendance:
				defaults = attendee.copy()
				member_id = defaults.pop('member_id')
				rsvp = defaults.pop('rsvp')
				
				attendee_instance, created = meetup.models.Attendee.objects.get_or_create(
					member_id=member_id,
					defaults=defaults
				)

				meetup.models.Attendance.objects.get_or_create(
					attendee_id=attendee_instance.pk,
					event_id=event_instance.pk,
					defaults={'rsvp': attendee['rsvp']}
				)

		meetup_instance.syncing = False
		meetup_instance.save()


def fetch_events(name: str, api_key: str) -> List[Dict]:
	"""Fetches the meetup attendance for a particular meetup and event.

	Args:
	    name (str): The meetup name which is also the path to the meetup page
	    api_key (str): A meetup API key

	Returns:
		A subset of event data from the meetup API
	"""
	uri = f"{settings.MEETUP_API_BASE_URI}{name}/events?sign=true&photo-host=public&status=past&key={api_key}"
	resp = requests.get(uri)
	resp.raise_for_status()

	events = []
	for event in resp.json():
		events.append({
			'event_id': event.get('id', None),
			'name': event.get('name', None),
			'time': event.get('time', None),
			'status': event.get('status', None),
			'local_date': event.get('local_date', None),
			'local_time': event.get('local_time', None),
			'yes_rsvp_count': event.get('yes_rsvp_count', None)
		})

	return events


def fetch_attendance(name: str, event_id: int, api_key: str) -> List[Dict]:
	"""Fetches the meetup attendance for a particular meetup and event.

	Args:
	    name (str): The meetup name which is also the path to the meetup page
	    event_id (int): A meetup event id
	    api_key (str): A meetup API key

	Returns:
		A subset of attendance data from the meetup API
	"""

	uri = f"{settings.MEETUP_API_BASE_URI}{name}/events/{event_id}/attendance?sign=true&key={api_key}"
	resp = requests.get(uri)
	resp.raise_for_status()

	attendance = []	
	for attendee in resp.json():
		rsvp = attendee.get('rsvp', None)
		
		if isinstance(rsvp, dict):
			rsvp = rsvp.get('response', None)

		attendance.append({
			'member_id': attendee['member']['id'],
			'name': attendee['member']['name'],
			'bio': attendee['member'].get('bio', None),
			'rsvp': rsvp

		})

	return attendance