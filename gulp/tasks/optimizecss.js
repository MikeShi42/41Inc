const gulp = require('gulp');
const nano = require('gulp-cssnano');
const size = require('gulp-size');
const sourcemaps = require('gulp-sourcemaps');


module.exports = (source, options, dist) => {
    return gulp.src(source)
        .pipe(sourcemaps.init({ loadMaps: true }))
        .pipe(nano(options))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(dist))
        .pipe(size());
};
