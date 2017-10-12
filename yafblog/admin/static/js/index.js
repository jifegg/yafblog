(function($){
    var YAFAdmin = {
        init: function() {
            var self = this; 
            self.initAddArticle();
            self.initAddTag();
            self.initLogin();
            self.initBtnUrl();
            self.initBtnModal();
            self.initCommonForm();
        },
        initBtnUrl:function(){
            $('.btn-url').click(function(){
                if ($(this).attr('data-target') == '_blank') {
                    window.open($(this).attr('data-url'));
                } else {
                    window.location.href = $(this).attr('data-url');
                }
            })
        },
        initBtnModal:function(){
            $('.btn-modal').click(function(){
                $.ajax({
                    type : "get",
                    url : $(this).attr('data-url'),
                    async : false,
                    success : function(data){
                        $('#modal').html(data).modal();
                    }
                });
            }) 
            submitForm('#modal-form', function(){
              $('#modal').on('hidden.bs.modal', function (e) {
                  window.location.reload();
              })
            });
        },
        initLogin: function(){
            if ($('#login-form').length) {
                submitForm('#login-form', function(data){
                    window.location.href = data.jump;
                });
            }

        },
        initAddTag: function(){
            if ($('#add-tag-form').length) {
                submitForm('#add-tag-form', function(data){
                    $('#add-tag-form').find('.tagname').val('');
                });
            }
        },
        initAddArticle: function(){
            if ($('#add-article-form').length) {
                var simplemde = new SimpleMDE({
                    element: $('#md-text')[0],
                    showIcons: ["code", "table"],
                    promptURLs: true,
                    autoDownloadFontAwesome: false,
                    spellChecker: false,
                    tabSize: 4,
                });
                var $parent = $('.tag-helper');
                var $input = $('.tag-helper-input');
                var $list = $('.tag-helper-list');
                var $panel = $('.tag-helper-panel');
                var $item = $('.tag-helper-item');
                submitForm('#add-article-form');
                $input.on('input propertychange',function(event){
                    $list.css("left", $input.position().left + "px")
                    $panel.addClass('hide');
                    if ($input.val() == '') {
                        $input.trigger('focus');
                        return false;
                    }
                    $.getJSON('/admin/tag/search/'+$input.val(), function(data){
                        if (data.code > 0) {
                            var html = ''
                            $.each(data.data, function(k,v){
                                if (k == 0) {
                                    html += '<li data-id='+v.id+' class="active">'+v.name+'</li>';
                                } else {
                                    html += '<li data-id='+v.id+'>'+v.name+'</li>';
                                }
                            });
                        } else {
                            var html = '<li class="add_tag active" data-name="'+$input.val()+'">添加标签 <b>'+$input.val()+'</b></li>';
                        }
                        $list.html(html);
                    })
                    $list.removeClass('hide');
                    event.preventDefault();
                    return false;
                })
                $input.focus(function(event){
                    $input.val('');
                    $panel.css("left", $input.position().left + "px")
                    $panel.removeClass('hide');
                    $list.addClass('hide');
                })
                $('body').on("click", function(e) {
                    if (! $(e.target).parents(".tag-helper-panel").length && ! $(e.target).parents(".tag-helper").length && !$(e.target).hasClass("tag-helper")) {
                        $panel.addClass('hide');
                    }
                });
                $list.on('click', 'li', function(){
                    var tag_name = $(this).html();
                    var tag_id = $(this).attr('data-id');
                    if (! tag_id) {
                        tag_name = $(this).attr('data-name');
                        $.ajax({
                            type : "post",
                            url : "/admin/tag/add",
                            data : {'name':tag_name},
                            dataType: "json",
                            async : false,
                            success : function(data){
                                if (data.code > 0) {
                                    tag_id = data.last_id;
                                } else {
                                    return false; 
                                }
                            }
                        });
                    } 
                    if (! $('#tag_'+tag_id).length) {
                        var item = '<span class="tag-helper-item">'+tag_name+'<span class="remove">×</span><input type="hidden" id="tag_'+tag_id+'" name="tag" value="'+tag_id+'"></span>';
                        $input.before(item);
                    }
                    $list.addClass('hide');
                    $input.val('');
                })
                $parent.on('click', '.tag-helper-item .remove', function(){
                    $(this).parent('.tag-helper-item').remove();
                })
                $panel.on('click', 'li', function(){
                    var tag_name = $(this).html();
                    var tag_id = $(this).attr('data-id');
                    if (! $('#tag_'+tag_id).length) {
                        var item = '<span class="tag-helper-item">'+tag_name+'<span class="remove">×</span><input type="hidden" id="tag_'+tag_id+'" name="tag" value="'+tag_id+'"></span>';
                        $input.before(item);
                    }
                    $list.addClass('hide');
                    $panel.addClass('hide');
                })
            }
        },
        initCommonForm:function(){
            $('.common-submit').each(function(k,v){
                submitForm('#'+$(v).parents('form').attr('id'));
            })
        }
    };
    window.YAFAdmin = YAFAdmin;
    YAFAdmin.init()
})(jQuery)

function submitForm(ele, callback) {
    $('body').on('submit', ele , function() {
        var $form = $(ele);
        var $submitBtn = $form.find('.submit');
        var $btnSpin = $submitBtn.find('i');
        var $btnMsg = $submitBtn.find('span');
        var $alert = $form.find('.alert');
        var btnmsg =$btnMsg.html();
        $submitBtn.attr('disabled', true);
        $btnMsg.html($submitBtn.attr('data-loadmsg'));
        $btnSpin.removeClass('hide');
        $.post($(this).attr('action'), $form.serialize(), function(data){
            $alert.removeClass('hide');
            if (data.code > 0) {
                if ($.isFunction(callback)) {
                    callback(data);
                }
                $alert.removeClass('alert-warning').addClass('alert-success').html('提交成功');
            } else {
                msg = data.msg ? data.msg : '提交失败';
                $alert.removeClass('alert-success').addClass('alert-warning').html(msg);
            }
            $submitBtn.removeAttr('disabled');
            $btnMsg.html(btnmsg);
            $btnSpin.addClass('hide');
        });
        return false;
    });
}
