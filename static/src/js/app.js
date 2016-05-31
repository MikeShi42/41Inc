/* global window */
window.videojs = require('video.js');
require('videojs-playlist');
require('videojs-playlist-ui');
window.jQuery = window.$ = require('jquery');
require('bootstrap-sass');

const $ = window.$;
const videojs = window.videojs;

const loadSeriesListings = videoID => {
    $.get(`/api/videos/${videoID}`, data => {
        console.log(data);
    });
};

$(() => {
    // fire up the plugin
    const player = videojs('video');

    loadSeriesListings(window.currentVideoID);

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
