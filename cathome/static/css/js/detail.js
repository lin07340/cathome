$(function () {
    var oExports = {
        initialize: fInitialize,
        encode: fEncode
    };
    oExports.initialize();

    function fInitialize() {
        var that = this;
        var sImageId = window.imageId;
        var commentCount = window.comment_count;
        var oCmtIpt = $('#jsCmt');
        var oListDv = $('ul.js-discuss-list');

        // 点击添加评论
        var bSubmit = false;
        $('#jsSubmit').on('click', function () {
            var sCmt = $.trim(oCmtIpt.val());
            // 评论为空不能提交
            if (!sCmt) {
                return alert('评论不能为空');
            }
            // 上一个提交没结束之前，不再提交新的评论
            if (bSubmit) {
                return;
            }
            bSubmit = true;
            $.ajax({
                url: '/add_comment/',
                type: 'post',
                dataType: 'json',
                data: {image_id: sImageId, content: sCmt}
            }).done(function (oResult) {
                if (oResult.code !== 0) {
                    return alert(oResult.msg || '提交失败，请重试');
                }
                // 清空输入框
                oCmtIpt.val('');
                // 渲染新的评论
                commentCount++;
                if (commentCount > 20) {
                    $("ul.discuss-list li:last").remove()
                }
                var sHtml1 = ['<li>',
                    '<a class=" icon-remove" title="删除评论" onclick="return confirm(\'确定删除该评论吗?\')" href="/remove_comment/'].join('');
                var sHtml2 = '';
                sHtml2 += oResult.comment_id.toString();
                console.log(sHtml2);
                var sHtml3 = ['/">', '</a>',
                    '<a class="_4zhc5 _iqaka" title="',
                    that.encode(oResult.user_name),
                    '" href="/profile/',
                    oResult.user_id,
                    '">', that.encode(oResult.user_name), ':</a> ',
                    '<span><span>', that.encode(sCmt), '</span></span>',
                    '</li>'].join('');
                var sHtml = sHtml1 + sHtml2 + sHtml3;
                oListDv.prepend(sHtml);
            }).fail(function (oResult) {
                alert(oResult.msg || '提交失败，请重试');
            }).always(function () {
                bSubmit = false;
            });
        });
    }

    function fEncode(sStr, bDecode) {
        var aReplace = ["&#39;", "'", "&quot;", '"', "&nbsp;", " ", "&gt;", ">", "&lt;", "<", "&amp;", "&", "&yen;", "¥"];
        !bDecode && aReplace.reverse();
        for (var i = 0, l = aReplace.length; i < l; i += 2) {
            sStr = sStr.replace(new RegExp(aReplace[i], 'g'), aReplace[i + 1]);
        }
        return sStr;
    }

});