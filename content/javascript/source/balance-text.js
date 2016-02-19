// restore "nbsp;" substituted for "<br>" (sic!) in "OS&nbsp;X"
(function () {
    var oldBalanceText = $.fn.balanceText

    $.fn.balanceText = function () {
        oldBalanceText.call(this, arguments)

        $('.balance-text').each(function () {
            var $x = $(this)
            $x.html($x.html().replace('OS<br data-owner="balance-text">X', 'OS&nbsp;X'))
        })
    }
})()
