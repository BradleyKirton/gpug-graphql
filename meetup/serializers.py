from rest_framework import serializers

import meetup.models


class MeetupSerializer(serializers.ModelSerializer):
    class Meta:
        model = meetup.models.Meetup
        fields = ("id", "name", "syncing")


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = meetup.models.Event
        fields = (
            "id",
            "event_id",
            "name",
            "time",
            "status",
            "local_date",
            "local_time",
            "yes_rsvp_count",
            "meetup",
        )


class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = meetup.models.Attendee
        fields = ("id", "member_id", "name", "bio")


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = meetup.models.Attendance
        fields = ("id", "event", "attendee", "rsvp")


class SyncMeetupPayloadSerializer(serializers.Serializer):
    meetup_id = serializers.IntegerField()
