import graphene
import typing


class Query(graphene.ObjectType):
	"""Used in introspection."""
	hello = graphene.String(description="Used in instrospection.")

	def resolve_hello(self, info: graphene.ResolveInfo, **kwargs: typing.Dict) -> str:
		return "Hello world"


# Schema consists of the following
# Root query
# Root mutation (optional)
# Root subscription (optional)
schema = graphene.Schema(query=Query, auto_camelcase=False)


if __name__ == '__main__':
	# GraphQL is introspectable by default
	introspected = schema.introspect()
	graphql_types = introspected['__schema']['types']
	query_details = next(filter(lambda x: x['name'] == 'Query', graphql_types))
	
	print('\nSchema introspection:')
	print('description:', query_details['description'])
	print('field name:', query_details['fields'][0]['name'])
	print('field description:', query_details['fields'][0]['description'])
	
	result = schema.execute("""
		query {
		    hello
		}
	""")

	print('\nExecution results:')
	print('errors:', result.errors)
	print('data:', dict(result.data))
