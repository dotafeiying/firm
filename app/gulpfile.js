'use strict';

const gulp = require('gulp');
const sass = require('gulp-sass')(require('sass'));
var del = require('del');
// 用来自动给 css 文件样式添加浏览器前缀
const autoprefixer = require('gulp-autoprefixer');
const rev = require('gulp-rev');
const uglify = require('gulp-uglify');
const plumber = require('gulp-plumber');
const revCollector = require('gulp-rev-collector');



// const { watch, series } = require('gulp');

var cssSrc = 'src/css/*.css',
    sassSrc = 'static/app/scss/**/*.scss',
    jsSrc = 'static/app/js/*.js',
    htmlSrc = 'templates/**/*.html';
var dir = 'dist';

var paths = {
    styles: {
        src: 'static/app/scss/**/*.scss',
        dest: 'static/app/css'
    },
    scripts: {
        src: 'static/app/js/*.js',
        dest: 'dist/js'
    },
    htmls: {
        src: 'templates/**/*.html',
        dest: 'templates'
    }
};

function clean() {
    // You can use multiple globbing patterns as you would with `gulp.src`,
    // for example if you are using del 2.0 or above, return its promise
    return del([ 'dist', 'rev' ]);
}

function styles() {
    return gulp.src(paths.styles.src)
        // .pipe(sass().on('error', sass.logError))
        .pipe(sass({outputStyle: 'expanded'}).on('error', sass.logError))
        .pipe(autoprefixer())
        .pipe(gulp.dest(paths.styles.dest))
        .pipe(rev())
        .pipe(gulp.dest('dist/css'))
        .pipe(rev.manifest())
        .pipe(gulp.dest('rev/css'));
}

function scripts() {
    return gulp.src(paths.scripts.src)
        .pipe(rev())
        .pipe(plumber())
        //压缩
        .pipe(uglify())
        .pipe(gulp.dest('dist/js'))
        .pipe(rev.manifest())
        .pipe(gulp.dest('rev/js'));
}

function htmls() {
    return gulp.src(['rev/**/*.json', paths.htmls.src])
        .pipe(plumber())
        .pipe(revCollector({
            replaceReved: true
        }))
        // .pipe(gulp.dest(dir+'/templates'));
        .pipe(gulp.dest('templates'));
}

function watch() {
    gulp.watch(paths.scripts.src, scripts);
    gulp.watch(paths.styles.src, styles);
    gulp.watch(['rev/**/*.json', paths.htmls.src], htmls)
}

/*
 * Specify if tasks run in series or parallel using `gulp.series` and `gulp.parallel`
 */
// var build = gulp.series(clean, styles);
var build = gulp.series(clean, gulp.parallel(styles, scripts), htmls);

exports.clean = clean;
exports.styles = styles;
exports.scripts = scripts;
exports.htmls = htmls;
exports.watch = watch;
exports.build = build;

exports.default = build;

// exports.buildStyles = styles;
// exports.watch = function () {
//     gulp.watch('static/app/scss/**/*.scss', series(clean, styles));
// };
// exports.default = series(clean, styles);
// exports.default = gulp.series(clean, gulp.parallel(styles, scripts));