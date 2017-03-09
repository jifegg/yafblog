$('#search-btn').click(function() {
    var keyword = $('#search-keyword').val();
    if ($.trim(keyword) == '') {
        return false;
    }
    var host = $('#search-form').attr('action');
    window.location.href = host + '/' + keyword;
    return false;
});
$.fn.tagcloud.defaults = {
  size: {start: 18, end: 38, unit: 'px'},
  color: {start: '#ccc', end: '#000'}
};

$(function () {
  $('.cloud a').tagcloud();
});
