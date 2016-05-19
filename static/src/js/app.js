/* global window */
window.videojs = require('video.js');
require('videojs-playlist');
require('videojs-playlist-ui');
window.jQuery = window.$ = require('jquery');
require('bootstrap-sass');

const $ = window.$;
const videojs = window.videojs;

const StripeHandler = require('./payments');

$(() => {
    // Stripe Checkout
    const stripeHandler = new StripeHandler();

    // Close Checkout on page navigation:
    $(window).on('popstate', () => {
        stripeHandler.close();
    });


    /**
     * Subscription
     */
    // Month Button
    let monthBtn = $('#month-sub-btn');
    let monthPrice = monthBtn.data('price');
    monthBtn.on('click', stripeHandler.handleSub('month', monthPrice));

    // Year Button
    let yearBtn = $('#year-sub-btn');
    let yearPrice = yearBtn.data('price');
    yearBtn.on('click', stripeHandler.handleSub('year', yearPrice));

    // fire up the plugin
    const player = videojs('video');
    player.playlist([{
        name: 'Disney\'s Oceans',
        description: 'Explore the depths of our planet\'s oceans. ',
        duration: 45,
        sources: [
            {src: 'http://vjs.zencdn.net/v/oceans.mp4', type: 'video/mp4'},
            {src: 'http://vjs.zencdn.net/v/oceans.webm', type: 'video/webm'}
        ],
        // you can use <picture> syntax to display responsive images
        thumbnail: [
            {
                srcset: 'http://lorempixel.com/400/300',
                type: 'image/jpeg'
            },
            {
                srcset: 'http://lorempixel.com/400/300'
            }
        ]
    }, {
        name: 'Sintel',
        description: 'The film follows a girl named Sintel who is searching for a baby dragon she calls Scales.',
        sources: [
            {src: 'http://media.w3.org/2010/05/sintel/trailer.mp4', type: 'video/mp4'},
            {src: 'http://media.w3.org/2010/05/sintel/trailer.webm', type: 'video/webm'},
            {src: 'http://media.w3.org/2010/05/sintel/trailer.ogv', type: 'video/ogg'}
        ],
        thumbnail: [
            {
                srcset: 'http://lorempixel.com/400/300'
            }
        ]
    }]);
    player.playlistUi();
});

