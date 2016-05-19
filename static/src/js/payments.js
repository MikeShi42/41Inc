const StripeCheckout = require('stripe-checkout');

// Stripe.setPublishableKey('pk_test_mNOqd6h6zKyrxeEo0pnQ0Zoj');

class StripeHandler {

    constructor() {
        this.handler = StripeCheckout.configure({
            key: 'pk_test_6pRNASCoBOKtIshFeQd4XMU',
            locale: 'auto'
        });
    }

    close() {
        this.handler.close();
    }

    handleSub(type) {
        return e => {
            e.preventDefault();

            let description = '';
            let price = 0.00;

            switch (type) {
                case 'year':
                    description = 'Yearly Subscription';
                    price = 12000;
                    break;
                case 'month':
                default:
                    description = 'Monthly Subscription';
                    price = 4000;
            }

            this.handler.open({
                name: '41 Inc.',
                description,
                amount: price,
                zipCode: true,
                panelLabel: 'Subscribe'
            });
        };
    }
}

module.exports = StripeHandler;
