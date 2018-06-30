import rest_framework.serializers
import meetup.models


class MeetupSerializer(rest_framework.serializers.ModelSerializer):
	class Meta:
		model = meetup.models.Meetup
		fields = (
			'id',
			'name',
			'syncing'
		)



class EventSerializer(rest_framework.serializers.ModelSerializer):
	class Meta:
		model = meetup.models.Event
		fields = (
			'id',
			'event_id',
			'name',
			'time',
			'status',
			'local_date',
			'local_time',
			'yes_rsvp_count',
			'meetup',
		)


class AttendeeSerializer(rest_framework.serializers.ModelSerializer):
	class Meta:
		model = meetup.models.Attendee
		fields = (
			'id',
			'member_id',
			'name',
			'bio'
		)


class AttendanceSerializer(rest_framework.serializers.ModelSerializer):
	class Meta:
		model = meetup.models.Attendance
		fields = (
			'id',
			'event',
			'attendee',
			'rsvp',
		)