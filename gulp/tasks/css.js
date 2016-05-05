/**
 * Dependencies
 */
const gulp   = require('gulp');
const sass   = require('gulp-sass');
const prefix = require('gulp-autoprefixer');

/**
 * Module body
 */
module.exports = (entry, config) => {
  config = config || {};
  config.sass = config.sass || {};
  config.autoprefixer = config.autoprefixer || {};

  return gulp.src(entry)
    .pipe(sass.sync(config.sass).on('error', sass.logError))
    .pipe(prefix(config.autoprefixer));
};
