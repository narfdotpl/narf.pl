$(function () {
    var $figures = $('figure')

    var adjustFigureMargins = function () {
        var width = $(window).width()
        var margin = Math.max(-192, Math.min(-12, -((width - 640) / 2)))

        $figures.css('margin-left',  margin + 'px')
        $figures.css('margin-right', margin + 'px')
    }

    adjustFigureMargins()

    $(window).resize(adjustFigureMargins)
})
