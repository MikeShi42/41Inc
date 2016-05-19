const StripeCheckout = require('stripe-checkout');

// Stripe.setPublishableKey('pk_test_mNOqd6h6zKyrxeEo0pnQ0Zoj');

class StripeHandler {

    constructor() {
        this.handler = StripeCheckout.configure({
            key: 'pk_test_ct2aMVE28fnn81LEj2fSJk2s',
            locale: 'auto'
        });
    }

    close() {
        this.handler.close();
    }

    handleSub(type, price) {
        return e => {
            e.preventDefault();

            let description = '';

            switch (type) {
                case 'year':
                    description = `Yearly Subscription - \$${price}/year`;
                    break;
                case 'month':
                default:
                    description = `Monthly Subscription - \$${price}/month`;
            }

            this.handler.open({
                name: '41 Inc.',
                description,
                zipCode: true,
                panelLabel: 'Subscribe Now'
            });
        };
    }
}

module.exports = StripeHandler;
