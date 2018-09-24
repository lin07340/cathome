$(function () {
    var oExports = {
        initialize: fInitialize,
        // 渲染更多数据
        renderMore: fRenderMore,
        // 请求数据
        requestData: fRequestData,
        // 简单的模板替换
        tpl: fTpl
    };
    // 初始化页面脚本
    oExports.initialize();

    function fInitialize() {
        var that = this;
        // 常用元素
        that.listEl = $('div.js-image-list');
        // 初始化数据
        that.uid = window.uid;
        that.page = 1;
        that.pageSize = 5;
        that.listHasNext = true;
        // 绑定事件
        $('.js-load-images').on('click', function (oEvent) {
            var oEl = $(oEvent.currentTarget);
            var sAttName = 'data-load';
            // 正在请求数据中，忽略点击事件
            if (oEl.attr(sAttName) === '1') {
                return;
            }
            // 增加标记，避免请求过程中的频繁点击
            oEl.attr(sAttName, '1');
            that.renderMore(function () {
                // 取消点击标记位，可以进行下一次加载
                oEl.removeAttr(sAttName);
                // 没有数据隐藏加载更多按钮
                !that.listHasNext && oEl.hide();
            });
        });
    }

    function fRenderMore(fCb) {
        var that = this;
        // 没有更多数据，不处理
        if (!that.listHasNext) {
            return;
        }
        that.requestData({
            uid: that.uid,
            page: that.page + 1,
            pageSize: that.pageSize,
            call: function (oResult) {
                // 是否有更多数据
                that.listHasNext = !!oResult.has_next && (oResult.images || []).length > 0;
                // 更新当前页面
                that.page++;
                // 渲染数据
                var sHtml = '';
                $.each(oResult.images, function (nIndex, oImage) {
                    var image_index = (that.page - 1) * 5 + nIndex + 1;
                    var sHtml1_1 = '';
                    sHtml1_1 += that.tpl([
                        '<article class="mod">',
                        '<header class="mod-hd">',
                        '<time class="time">#{created_time}</time>',
                        '<a href="/profile/#{user_id}" class="avatar">',
                        '<img src="#{head_url}">',
                        '</a>',
                        '<div class="profile-info">',
                        '<a title="#{username}" href="/profile/#{user_id}">#{username}</a>',
                        '</div>',
                        '</header>',
                        '<div class="mod-bd">',
                        '<div class="img-box">',
                        '<a href="/image/#{id}">',
                        '<img src="#{url}">',
                        '</a>',
                        '</div>',
                        '</div>',
                        '<div class="mod-ft">',
                        '<ul class="discuss-list ">',
                        '<li class="more-discuss">',
                        '<a href="/image/#{id}/">',
                        '<span>全部 </span><span class="length-'
                    ].join(''), oImage);
                    var sHtml1_2 = '';
                    sHtml1_2 += that.tpl([
                        '">',
                        '#{comment_count}',
                        '</span>',
                        '<span> 条评论</span></a>',
                        '</li>',
                        '<tag class="content_detail js-discuss-list-'
                    ].join(''), oImage);
                    var sHtml1_3 = '';
                    sHtml1_3 += that.tpl([
                        '">'
                    ].join(''), oImage);
                    //console.log(image_index);
                    var sHtml1 = sHtml1_1 + image_index.toString() + sHtml1_2 + image_index.toString() + sHtml1_3;

                    //加载评论
                    var sHtml2 = '';
                    for (var i = 0; i < oImage.show_comments_count; i++) {
                        comment = oImage.comments[i];
                        //console.log(comment);
                        sHtml2 += that.tpl([
                            '<li>',
                            '<a class="_4zhc5 _iqaka" title="#{username}" href="/profile/#{from_user_id}" data-reactid="">#{username}:</a>',
                            '<span>',
                            '<span>#{content}</span>',
                            '</span>',
                            '</li>'].join(''), comment);
                    }

                    //评论区
                    var sHtml3 = '';
                    var sHtml3_1 = '';
                    var sHtml3_2 = '';
                    var sHtml3_3 = '';
                    var sHtml3_4 = '';
                    sHtml3_1 += that.tpl(['</tag>',
                        '</ul>',
                        '<section class="discuss-edit">',
                        '<a class="icon-heart"></a>',
                        '<form>',
                        '<input placeholder="添加评论..." id="jsCmt-'].join(''), oImage);
                    sHtml3_2 += that.tpl([
                        '" type="text">',
                        '<input id="js-image-id-'].join(''), oImage);
                    sHtml3_3 += that.tpl([
                        '" type="text" style="display: none" value="#{id}">',
                        '</form>',
                        '<button class="more-info"  id="jsSubmit-'].join(''), oImage);
                    sHtml3_4 += that.tpl([
                        '">更多选项</button>',
                        '</section>',
                        '</div>',
                        '</article>'].join(''), oImage);
                    sHtml3 = sHtml3_1 + image_index.toString() + sHtml3_2 + image_index.toString()
                        + sHtml3_3 + image_index.toString() + sHtml3_4;
                    sHtml += sHtml1 + sHtml2 + sHtml3;
                });
                sHtml && that.listEl.append(sHtml);
                sHtml && that.listEl.append(freload());
            },
            error: function () {
                alert('出现错误，请稍后重试');
            },
            always: fCb
        });
    }

    function fRequestData(oConf) {
        var that = this;
        var sUrl = '/index/' + oConf.page + '/' + oConf.pageSize + '/';
        $.ajax({url: sUrl, dataType: 'json'}).done(oConf.call).fail(oConf.error).always(oConf.always);
        //that.reload();
    }

    function fTpl(sTpl, oData) {
        var that = this;
        sTpl = $.trim(sTpl);
        return sTpl.replace(/#{(.*?)}/g, function (sStr, sName) {
            return oData[sName] === undefined || oData[sName] === null ? '' : oData[sName];
        });
    }

    function freload() {
        var script_type = "text/javascript";
        var script_src = "/static/css/js/index_add_comments.js";
        var strjs = '';
        strjs += '<script type="';
        strjs += script_type;
        strjs += '" src="';
        strjs += script_src;
        strjs += '"></scrip';
        strjs += 't>';
        return strjs;
    }
});
