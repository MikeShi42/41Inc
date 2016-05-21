from rauth import OAuth2Service

from fourtyone import settings

stripe_connect_service = OAuth2Service(
    name='stripe',
    client_id=settings.STRIPE_CLIENT_ID,
    client_secret=settings.STRIPE_CLIENT_SECRET,
    authorize_url='https://connect.stripe.com/oauth/authorize',
    access_token_url='https://connect.stripe.com/oauth/token',
    base_url='https://api.stripe.com/',
)