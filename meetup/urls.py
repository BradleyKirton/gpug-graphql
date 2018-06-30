import django.urls
import meetup.views
import meetup.schema
import meetup.views
import rest_framework.routers
import graphene
import graphene_django.views


# Setup the DRF routes
router = rest_framework.routers.DefaultRouter()
router.register('meetups', meetup.views.MeetupViewSet)
router.register('events', meetup.views.EventViewSet)
router.register('attendees', meetup.views.AttendeeViewSet)
router.register('attendance', meetup.views.AttendanceViewSet)


# Create the graphql view (No integration with DRF)
schema = graphene.Schema(meetup.schema.Query, auto_camelcase=False)
graphql_view = graphene_django.views.GraphQLView.as_view(schema=schema, graphiql=True)


# Create the DRF integrated graphql view
drf_graphql_view = meetup.views.RestGraphQL.as_view(schema=schema)


urlpatterns = [
	django.urls.path('tasks/', meetup.views.Task.as_view(), name='tasks-page'),
	django.urls.path('', graphql_view),
	django.urls.path('api/', django.urls.include(router.urls)),
	django.urls.path('api/graphql/', drf_graphql_view)
]