/* eslint-disable prefer-arrow-callback */
/* eslint-disable func-names */
const gulp = require('gulp');
const babel = require('gulp-babel');
const minify = require('gulp-minify');
const uglify = require('gulp-uglify');
const cleanCss = require('gulp-clean-css');
const imageMin = require('gulp-imagemin');
const clean = require('gulp-clean');

gulp.task('clean', function () {
  return gulp.src('dist', { read: false, allowEmpty: true })
    .pipe(clean());
});

gulp.task('directories', function () {
  return gulp.src('src/public/**/*', { read: false })
    .pipe(gulp.dest('dist/'));
});

gulp.task('copy-js', function () {
  return gulp.src('src/public/js/jquery.prettyPhoto.js')
    .pipe(gulp.dest('dist/js/'));
});

gulp.task('minify-js', function () {
  return gulp.src(['src/public/js/**/*.js', 'src/public/contactform/*.js', '!src/public/js/jquery.prettyPhoto.js'])
    .pipe(babel())
    .pipe(minify({
      ext: {
        min: '.js', // Set the file extension for minified files to just .js
      },
      noSource: true, // Don’t output a copy of the source file
    }))
    .pipe(uglify())
    .pipe(gulp.dest(function (file) {
      if (file.path.indexOf('src/public/js') !== -1) {
        return 'dist/js/';
      } else if (file.path.indexOf('src/public/contactform') !== -1) {
        return 'dist/contactform/';
      }
    }));
});

gulp.task('clean-css', function () {
  return gulp.src(['src/public/css/**/*.css', 'src/public/color/*.css'])
    .pipe(cleanCss())
    .pipe(gulp.dest(function (file) {
      if (file.path.indexOf('src/public/css') !== -1) {
        return 'dist/css/';
      } else if (file.path.indexOf('src/public/color') !== -1) {
        return 'dist/color/';
      }
    }));
});

gulp.task('opt-images', function () {
  return gulp.src(['src/public/img/**/*', 'src/public/ico/**/*'])
    .pipe(imageMin())
    .pipe(gulp.dest(function (file) {
      if (file.path.indexOf('src/public/img') !== -1) {
        return 'dist/img/';
      } else if (file.path.indexOf('src/public/ico') !== -1) {
        return 'dist/ico/';
      }
    }));
});

gulp.task('clean-fonts', function () {
  return gulp.src('src/public/fonts/**/*')
    .pipe(gulp.dest('dist/fonts/'));
});

gulp.task('default', gulp.series('clean', 'directories', 'copy-js', 'minify-js', 'clean-css', 'opt-images', 'clean-fonts'));