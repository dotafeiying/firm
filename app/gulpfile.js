//引入gulp和gulp插件
var gulp = require('gulp'),
    runSequence = require('run-sequence'),
    rev = require('gulp-rev'),
    revCollector = require('gulp-rev-collector'),
    sass = require('gulp-sass'),
    autoprefixer = require('gulp-autoprefixer'),
    minifycss = require('gulp-minify-css'),
    // jshint = require('gulp-jshint'),
    uglify = require('gulp-uglify'),
    imagemin = require('gulp-imagemin'),
    // rename = require('gulp-rename'),
    clean = require('gulp-clean'),
    del  = require('del'),
    //错误处理提示插件
    plumber = require('gulp-plumber'),
    compass = require('gulp-compass'),
    concat = require('gulp-concat');

//定义css、js源文件路径
var cssSrc = 'src/css/*.css',
    sassSrc = 'static/app/scss/**/*.scss',
    jsSrc = 'static/app/js/*.js',
    htmlSrc = 'templates/**/*.html';
// var dir = '../app/static/app/';    //对目标根目录进行变量
var dir = 'dist';    //对目标根目录进行变量

//清空目标文件
gulp.task('cleanDst', function () {
    return gulp.src([dir,'rev'], {read: false})
        .pipe(clean());
    // return gulp.src('rev', {read: false})
    //     .pipe(clean());
});

//sass转换为css
gulp.task('sass', function(){
    // del([dir+'/css/*.css'],{force: true});
    return gulp.src(sassSrc)
        // .pipe(plumber())
        .pipe(sass({outputStyle: 'expanded'}).on('error', sass.logError))
        .pipe(autoprefixer())
        .pipe(gulp.dest('static/app/css'))
        .pipe(rev())
        .pipe(gulp.dest(dir+'/css'))
        .pipe(rev.manifest())
        .pipe(gulp.dest('rev/css'));
});

//CSS生成文件hash编码并生成 rev-manifest.json文件名对照映射
// gulp.task('revCss', function(){
//     return gulp.src(cssSrc)
//         .pipe(rev())
//         .pipe(gulp.dest('dist/css'))
//         .pipe(rev.manifest())
//         .pipe(gulp.dest('rev/css'));
// });


//js生成文件hash编码并生成 rev-manifest.json文件名对照映射
gulp.task('revJs', function(){
    return gulp.src(jsSrc)
        .pipe(rev())
        .pipe(plumber())
        //压缩
        .pipe(uglify())
        .pipe(gulp.dest(dir+'/js'))
        .pipe(rev.manifest())
        .pipe(gulp.dest('rev/js'));
});


//Html替换css、js文件版本
gulp.task('revHtml', function () {
    return gulp.src(['rev/**/*.json', htmlSrc])
        .pipe(plumber())
        .pipe(revCollector({
            replaceReved: true
        }))
        // .pipe(gulp.dest(dir+'/templates'));
        .pipe(gulp.dest('templates'));
});

gulp.task('watch',function(){
    // gulp.watch(cssSrc, ['revCss']);     //监视html文件，如果发生变化就进行复制
    gulp.watch(sassSrc, ['sass']);       //监视css文件，如果发生变化就进行复制
    gulp.watch(jsSrc, ['revJs']);       //监视css文件，如果发生变化就进行复制
    // gulp.watch('img/*.{jpg,png}',['copyImg']);      //监视图片，如果发生变化就进行复制
    // gulp.watch('js/*.js', ['copyJs']);      //监视js文件，如果发生变化就进行复制
    gulp.watch('{rev/**/*.json,templates/**/*.html}', ['revHtml'])     //监视json文件和html文件，如果发生变化就进行hash命名，和引用更改
});


//开发构建
gulp.task('dev', function (done) {
    condition = false;
    runSequence(
        ['cleanDst'],
        ['sass'],
        // ['revCss'],
        ['revJs'],
        ['revHtml'],
        ['watch'],
        done);
});


gulp.task('default', ['dev']);

