import meetup.models

from django.contrib import admin


# Register the models on the admin site
admin.site.register(meetup.models.Meetup)
admin.site.register(meetup.models.Event)
admin.site.register(meetup.models.Attendee)
admin.site.register(meetup.models.Attendance)