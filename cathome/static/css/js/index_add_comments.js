$(function () {
    var oExports = {
        initialize: fInitialize,
        encode: fEncode
    };
    oExports.initialize();

    function fInitialize() {
        var that = this;
        var num = $('ul.discuss-list');
        console.log(num);
        for (i = 1; i <= num.length; i++) {
            //var sImageId = $('#js-image-id-' + i);
            //console.log(sImageId.val())
            //var oCmtIpt = $('#jsCmt-' + i);
            //var oListDv = $('#js-discuss-list-' + i);
            // 点击添加评论
            var bSubmit = false;
            $('#jsSubmit-' + i).unbind();
            $('#jsSubmit-' + i).on('click', function () {
                var control_id = $(this).attr('id')
                var id = control_id.substring(9)
                console.log(id)
                var sImageId = $('#js-image-id-' + id).val();
                console.log(sImageId)
                var oCmtIpt = $('#jsCmt-' + id);
                console.log(oCmtIpt.val())
                var oListDv = $('.js-discuss-list-' + id);

                //var sCmt = $.trim(oCmtIpt.val());
                //alert(sCmt)
                sCmt = oCmtIpt.val()
                console.log(sCmt)
                // 评论为空不能提交
                if (!sCmt) {
                    console.log('pinglun: ' + id + oCmtIpt.attr('id'))
                    return alert('评论不能为空');
                    //continue;
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
                    console.log(oResult.code);
                    if (oResult.code !== 0) {
                        if (oResult.code === -2) {
                            return alert('请登陆后重试！');
                        }
                        return alert(oResult.msg || '提交失败，请重试');
                    }
                    // 清空输入框
                    oCmtIpt.val('');

                    // 修改评论数
                    var counts = $(".length-" + id).text()
                    $(".length-" + id).text(parseInt(counts, 10) + 1);
                    if (counts >= 3) {
                        $(".content_detail li:last-child").remove()
                        console.log(counts)
                    }
                    // 渲染新的评论
                    var sHtml = [
                        '<li>',
                        '<a class="_4zhc5 _iqaka" title="', that.encode(oResult.user_name), '" href="/profile/', oResult.user_id, '">', that.encode(oResult.user_name), ':</a> ',
                        '<span><span>', that.encode(sCmt), '</span></span>',
                        '</li>'].join('');
                    oListDv.prepend(sHtml);
                }).fail(function (oResult) {
                    alert(oResult.msg || '提交失败，请重试');
                }).always(function () {
                    bSubmit = false;
                });
            });
        }
    }

    function fEncode(sStr, bDecode) {
        var aReplace = ["&#39;", "'", "&quot;", '"', "&nbsp;", " ", "&gt;", ">", "&lt;", "<", "&amp;", "&", "&yen;", "¥"];
        !bDecode && aReplace.reverse();
        for (var i = 0, l = aReplace.length; i < l; i += 2) {
            sStr = sStr.replace(new RegExp(aReplace[i], 'g'), aReplace[i + 1]);
        }
        return sStr;
    };

});