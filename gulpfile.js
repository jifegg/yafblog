var gulp = require('gulp');
var sass = require('gulp-sass');
var csso = require('gulp-csso');
var uglify = require('gulp-uglify');
var concat = require('gulp-concat');
var replace = require('gulp-replace');


var bootstrap_js_path = 'node_modules/bootstrap/js/dist/';
var simplemde_path = 'node_modules/simplemde/dist/';
var home_js_path = 'yafblog/home/static/js/';
var home_css_path = 'yafblog/home/static/css/';
var home_sass_path = 'yafblog/home/static/sass/';
var admin_js_path = 'yafblog/admin/static/js/';
var admin_css_path = 'yafblog/admin/static/css/';
var admin_sass_path = 'yafblog/admin/static/sass/';
var css_path = {
    'home' : {
        src : home_sass_path+'*.scss',
        dest: home_css_path
    },
    'admin' : {
        src : admin_sass_path+'*.scss',
        dest: admin_css_path,
    }
}
var js_path = {
    'home' : {
        src:[
                bootstrap_js_path+'util.js',
                bootstrap_js_path+'collapse.js',
                home_js_path+'jquery.tagcloud.js',
                home_js_path+'index.js'
        ],
        dest:home_js_path
    },
    'admin' : {
        src:[
                bootstrap_js_path+'util.js',
                bootstrap_js_path+'collapse.js',
                bootstrap_js_path+'alert.js',
                bootstrap_js_path+'modal.js',
                admin_js_path+'index.js'
        ],
        dest:admin_js_path
    }
}
gulp.task('sass', function(cb){
    for (var key in css_path){
        var stream = gulp.src(css_path[key].src)
            .pipe(sass())
            .pipe(csso())
            .pipe(gulp.dest(css_path[key].dest))
    }
    return stream
});
gulp.task('concat_css', ['sass'], function(){
    return gulp.src([simplemde_path+'simplemde.min.css',admin_css_path+'main.css'])
        .pipe(concat('main.css'))
        .pipe(gulp.dest(admin_css_path))
})
gulp.task('js', function(){
    for (var key in css_path){
        stream = gulp.src(js_path[key].src)
            .pipe(concat('main.min.js'))
            .pipe(uglify())
            .pipe(gulp.dest(js_path[key].dest))
    }
    return stream
});
gulp.task('concat_js', ['js'], function(){
    return gulp.src([simplemde_path+'simplemde.min.js',admin_js_path+'main.min.js'])
        .pipe(concat('main.min.js'))
        .pipe(gulp.dest(admin_js_path))
})

gulp.task('watch', function() {
    gulp.watch([css_path.home.src, css_path.admin.src], ['css']);
    gulp.watch([js_path.home.src, js_path.admin.src], ['js']);
});
gulp.task('default', ['sass', 'concat_css', 'js', 'concat_js']);


