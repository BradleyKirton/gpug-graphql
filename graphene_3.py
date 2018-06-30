import graphene
import typing


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


class CreateArtist(graphene.Mutation):
    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()

    status = graphene.String()
    artist = graphene.Field(lambda: ArtistType)

    def mutate(self, info: graphene.ResolveInfo, first_name: str, last_name: str):
        artist = ArtistType(first_name=first_name, last_name=last_name)
       
        return CreateArtist(artist=artist, status='OK')


class SendEmail(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    status = graphene.String()
    
    def mutate(self, info: graphene.ResolveInfo, name: str):
        print('\nSending email:')
        print(f'Hello {name}, please send me your bank details.\n')

        return SendEmail(status="OK")


class Mutations(graphene.ObjectType):
    create_artist = CreateArtist.Field()
    send_email = SendEmail.Field()


schema = graphene.Schema(mutation=Mutations, auto_camelcase=False)


if __name__ == '__main__':
    # Call the create artist mutation
    result = schema.execute("""
        mutation call_create_artist {
            create_artist(first_name: "John", last_name: "Lennon") {
                artist {
                    first_name
                    last_name
                }
                status
            }
        }
    """)

    print("Create artist mutation:", result.data)

    # Call the send email mutation
    result = schema.execute("""
        mutation call_send_email {
            send_email(name: "Bradley") {
                status
            }
        }
    """)

    print("Send email mutation:", result.data)