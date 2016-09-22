$(function () {
    for (const [selector, maxWidth, offset] of [
        ['figure:not(.figure4608)', 1024, 0],
        ['.figure4608', 4608/2, 0],
        ['ul.gallery', 1024, -2],
    ]) {
        const $el = $(selector)

        const adjustMargins = function () {
            const contentWidth = 640
            const getMargin = (width) => (contentWidth - width) / 2

            const width = $(window).width()
            const minMargin = getMargin(maxWidth)
            const maxMargin = -12
            const margin = Math.max(minMargin, Math.min(maxMargin, getMargin(width))) + offset;

            $el.css('margin-left',  margin + 'px')
            $el.css('margin-right', margin + 'px')
        }

        adjustMargins()

        $(window).resize(adjustMargins)
    }
})
