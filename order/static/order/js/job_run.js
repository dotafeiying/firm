function review_status(order_no) {
    (function ($) {
        $(`#result_list .field-order_no:contains(${order_no})`).parent('tr').addClass('selected')
        var csrf = $('input[name="csrfmiddlewaretoken"]').val()
        var loading = layer.load(1);
        $.post('/order/review_status',{'order_no': order_no, 'csrfmiddlewaretoken': csrf}, function (data) {
            layer.close(loading);
            console.log(data);
            if (data.res == 0) {
                // $(`#result_list .field-order_no:contains(${order_no})`).parent('tr').removeClass('selected')
                layer.msg(data.message)
            } else {
                layer.alert(order_no + data.errmsg, {icon: 2});
            }

        })
    })(django.jQuery);
}

function order_refund(order_no, total_price) {
    (function ($) {
        $(`#result_list .field-order_no:contains(${order_no})`).parent('tr').addClass('selected')
        layer.open({
            content: `<p>确定对订单 ${order_no} 进行退款？退款金额 <span style="color: red">${total_price}</span> 元</p>`,
            // content: "<p>确定对订单 " + order_no + " 进行退款？退款金额" + total_price + "元</p>",
            btn: ['确定', '取消'],
            yes: function (idx, layero) {
                var refundLoading = layer.load(1);
                var csrf = $('input[name="csrfmiddlewaretoken"]').val()
                $.post('/order/refund', {'order_no': order_no, 'csrfmiddlewaretoken': csrf}, function (data) {
                    layer.close(refundLoading);
                    console.log(data);
                    if (data.res == 0) {
                        layer.alert(order_no + '退款成功', {icon: 1});
                        $(`#result_list .field-order_no:contains(${order_no})`).siblings('td.field-color_status').find('span').css('background-color','black').text('已退款')
                        // layer.alert(order_no + '退款成功', function (index) {
                        //     layer.close(index);
                        //     $(`#result_list .field-order_no:contains(${order_no})`).siblings('td.field-color_status').find('span').css('background-color','black').text('已退款')
                        //     // location.reload()
                        // });
                    } else {
                        layer.alert(order_no + data.errmsg, {icon: 2});
                    }
                })
                layer.close(idx); //如果设定了yes回调，需进行手工关闭
            },
            btn2: function (index, layero) {
                $(`#result_list .field-order_no:contains(${order_no})`).parent('tr').removeClass('selected')
                //return false 开启该代码可禁止点击该按钮关闭
            }
        });

    })(django.jQuery);
}

