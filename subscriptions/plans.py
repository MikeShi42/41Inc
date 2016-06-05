"""Manage plan updates with the stripe API"""

import stripe

from fourtyone import settings


def setup(stripe_account, price_month, price_year, plan_id_month=settings.PLAN_ID_MONTHLY,
          plan_id_year=settings.PLAN_ID_YEARLY):
    """
    Setup plans
    :param price_year:
    :param plan_id_year:
    :param plan_id_month:
    :param price_month:
    :type stripe_account: str
    :return:
    """

    # Set key
    stripe.api_key = settings.STRIPE_CLIENT_SECRET

    # Create monthly plan
    __create_or_update_plan(stripe_account=stripe_account, plan_name='Premium Subscription (Monthly)',
                            plan_id=plan_id_month,
                            plan_price=price_month,
                            plan_interval='month')
    __create_or_update_plan(stripe_account=stripe_account, plan_name='Premium Subscription (Yearly)',
                            plan_id=plan_id_year,
                            plan_price=price_year,
                            plan_interval='year')


def __create_or_update_plan(stripe_account, plan_name, plan_id, plan_price, plan_interval):
    create = False

    try:
        # Get plan
        plan = stripe.Plan.retrieve(plan_id, stripe_account=stripe_account)

        # Delete if there is a difference in existing and new plan
        if plan.amount != plan_price:
            plan.delete()

            # Need to create new plan
            create = True

        # Update name if different
        else:
            if plan.name != plan_name:
                plan.name = plan_name
                plan.save()

    except stripe.error.InvalidRequestError as e:
        # Check if doesn't exist and create if doesn't exist
        if e.http_status == 404:
            create = True

    # Check if we need to create plan
    if create:
        # Create plan
        stripe.Plan.create(
            amount=plan_price,
            interval=plan_interval,
            name=plan_name,
            currency="usd",
            id=plan_id,
            stripe_account=stripe_account
        )
