$(function () {
    for (let [selector, maxWidth, offset] of [
        ['figure:not(.full-width)', 1024, 0],
        ['figure.full-width', 0, 0],
        ['ul.gallery', 1024, -2],
    ]) {
        const $el = $(selector)
        if ($el.length === 0) {
            continue
        }

        if (maxWidth === 0) {
            maxWidth = $el.find('img')[0].naturalWidth / 2
        }

        const adjustMargins = function () {
            const windowWidth = $(window).width()
            const contentWidth = 640
            const effectiveContentWidth = Math.min(contentWidth, windowWidth)

            const getMargin = (width) => {
                let margin = (effectiveContentWidth - width) / 2

                return Math.min(margin, -12) + offset
            }

            const width = Math.min(windowWidth, maxWidth);
            const margin = getMargin(width);

            $el.css('margin-left',  margin + 'px')
            $el.css('margin-right', margin + 'px')
        }

        adjustMargins()

        $(window).resize(adjustMargins)
    }
})
