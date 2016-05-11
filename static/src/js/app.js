/* global window */
window.videojs = require('video.js');
require('videojs-playlist');
require('videojs-playlist-ui');
window.jQuery = window.$ = require('jquery');
require('bootstrap-sass');

const $ = window.$;
const videojs = window.videojs;

$(() => {
    // fire up the plugin
    const player = videojs('video');
    player.playlist([{
        name: 'Disney\'s Oceans',
        description: 'Explore the depths of our planet\'s oceans. ' +
        'Experience the stories that connect their world to ours. ' +
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, ' +
        'sed do eiusmod tempor incididunt ut labore et dolore magna ' +
        'aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco ' +
        'laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure ' +
        'dolor in reprehenderit in voluptate velit esse cillum dolore eu ' +
        'fugiat nulla pariatur. Excepteur sint occaecat cupidatat non ' +
        'proident, sunt in culpa qui officia deserunt mollit anim id est ' +
        'laborum.',
        duration: 45,
        sources: [
            {src: 'http://vjs.zencdn.net/v/oceans.mp4', type: 'video/mp4'},
            {src: 'http://vjs.zencdn.net/v/oceans.webm', type: 'video/webm'}
        ],
        // you can use <picture> syntax to display responsive images
        thumbnail: [
            {
                srcset: 'http://lorempixel.com/400/400',
                type: 'image/jpeg',
                media: '(min-width: 400px;)'
            },
            {
                srcset: 'http://lorempixel.com/400/400'
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
        thumbnail: false
    },
        // This is a really underspecified video to demonstrate the
        // behavior when optional parameters are missing. You'll get prettier
        // results with more video metadata!
        {
            sources: []
        }]);
    player.playlistUi();
});

