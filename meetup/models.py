from django.db import models


class Meetup(models.Model):
	name = models.CharField(max_length=250)
	syncing = models.BooleanField(default=False)


class Event(models.Model):
	STATUS_TYPES = (
		('cancelled', 'cancelled'),
		('draft', 'draft'),
		('past', 'past'),
		('proposed', 'proposed'),
		('suggested', 'suggested'),
		('upcoming', 'upcoming')
	)

	event_id = models.CharField(max_length=25)
	name = models.TextField(null=True)
	time = models.CharField(max_length=10)
	status = models.CharField(max_length=10, choices=STATUS_TYPES)
	local_date = models.DateField(null=True)
	local_time = models.TimeField(null=True)
	yes_rsvp_count = models.IntegerField(null=True)
	meetup = models.ForeignKey(Meetup, on_delete=models.CASCADE)


class Attendee(models.Model):
	member_id = models.IntegerField()
	name = models.TextField()
	bio = models.TextField(null=True)


class Attendance(models.Model):
	RSVP_TYPES = (
		('yes', 'yes'),
		('no', 'no'),
		('waitlist', 'waitlist')
	)

	event = models.ForeignKey(Event, on_delete=models.CASCADE)
	attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
	rsvp = models.CharField(max_length=3, choices=RSVP_TYPES, null=True)