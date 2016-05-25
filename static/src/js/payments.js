const StripeCheckout = require('stripe-checkout');
const $ = require('jquery');

class StripeHandler {

    constructor(window) {
        this.window = window;
        this.handler = StripeCheckout.configure({
            key: this.window.STRIPE_PUBLIC_KEY,
            locale: 'auto',
            token: token => {
                $.post(this.window.location, {token: token.id}, () => {

                });
            }
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
