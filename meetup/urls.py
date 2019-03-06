import django.urls
import meetup.views
import meetup.schema
import meetup.views
import rest_framework.reverse
import rest_framework.request
import rest_framework.response
import rest_framework.views
import rest_framework.routers
import graphene
import graphene_django.views


# Setup the DRF routes
router = rest_framework.routers.SimpleRouter()
router.register("meetups", meetup.views.MeetupViewSet, base_name="meetup")
router.register("events", meetup.views.EventViewSet, base_name="event")
router.register("attendees", meetup.views.AttendeeViewSet, base_name="attendee")
router.register("attendance", meetup.views.AttendanceViewSet, base_name="attendance")


class RootApiView(rest_framework.views.APIView):
    def get(
        self, request: rest_framework.request.Request
    ) -> rest_framework.response.Response:
        routes = {
            "meetups": rest_framework.reverse.reverse("meetup-list", request=request),
            "sync-meetup": rest_framework.reverse.reverse(
                "sync-meetup", request=request
            ),
            "events": rest_framework.reverse.reverse("event-list", request=request),
            "attendees": rest_framework.reverse.reverse(
                "attendee-list", request=request
            ),
            "attendance": rest_framework.reverse.reverse(
                "attendance-list", request=request
            ),
            "graphql-drf": rest_framework.reverse.reverse(
                "graphql-drf", request=request
            ),
        }

        return rest_framework.response.Response(routes)


# Create the graphql view (No integration with DRF)
schema = graphene.Schema(meetup.schema.Query, auto_camelcase=False)
graphql_view = graphene_django.views.GraphQLView.as_view(schema=schema, graphiql=True)


# Create the DRF integrated graphql view
drf_graphql_view = meetup.views.RestGraphQL.as_view(schema=schema)


urlpatterns = [
    django.urls.path("", meetup.views.Task.as_view(), name="tasks-page"),
    django.urls.path("api/", django.urls.include(router.urls)),
    django.urls.path("api/sync-meetup/", meetup.views.sync_meetup, name="sync-meetup"),
    django.urls.path("api/", RootApiView.as_view()),
    django.urls.path("api/graphql/", drf_graphql_view, name="graphql-drf"),
]
