import stripe

from fourtyone import settings

"""Handles a subscription request from subscriber"""
def process_subscription(request, pk):
    # Import API key
    stripe.api_key = settings.STRIPE_CLIENT_SECRET

    # Get token from request
    token = request.POST['token']

    # Get email form user
    email = request.user.email

    # Create customer and subscribe to plan
    customer = stripe.Customer.create(
        source=token,
        plan="gold",
        email=email
    )