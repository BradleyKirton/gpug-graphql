import graphene
import typing


artists = [
	{'first_name': 'Ben', 'last_name': 'Howard'},
	{'first_name': 'Damien', 'last_name': 'Rice'},
	{'first_name': 'Noah', 'last_name': 'Gundersen'},
]


class ArtistType(graphene.ObjectType):
	"""Artist type.

	An artist is descibed by their first and last name.
	"""
	first_name = graphene.String()
	last_name = graphene.String()

	def resolve_first_name(self, info: graphene.ResolveInfo, **kwargs: typing.Dict) -> str:
		return self.first_name

	def resolve_last_name(self, info: graphene.ResolveInfo, **kwargs: typing.Dict) -> str:
		return self.last_name


class ArtistQuery(graphene.ObjectType):
	"""Artist query.

	Exposes the artist data.
	"""
	artists = graphene.List(ArtistType)

	def resolve_artists(self, info: graphene.ResolveInfo, **kwargs: typing.Dict) -> str:
		return [ArtistType(**artist) for artist in artists]


class Query(ArtistQuery, graphene.ObjectType):
	pass


schema = graphene.Schema(query=Query, auto_camelcase=False)


if __name__ == '__main__':
	result = schema.execute("""
		query {
			artists {
				first_name
			}
		}
	""")

	print('query 1:', result.data)

	result = schema.execute("""
		query {
			artists {
				last_name
			}
		}
	""")

	print('query 2:', result.data)

	result = schema.execute("""
		query {
			artists {
				first_name
				last_name
			}
		}
	""")

	print('query 3:', result.data)