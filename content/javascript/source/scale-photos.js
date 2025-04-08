$(window).on("load", function () {
    const reguralWidth = 1024
    for (let [selector, maxWidth, offset] of [
        ['figure:not(.full-width)', reguralWidth, 0],
        ['figure.full-width', 0, 0],
        ['figure.full-ish-width', -80 * 2, 0],
        ['ul.gallery', reguralWidth, -2],
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

            // Don't mutate the original `maxWidth` because it will interfere
            // with future calls. First add margins above the regular width,
            // then increase the width.
            let newMaxWidth = maxWidth
            if (maxWidth < 0) {
                const sideMargins = -maxWidth
                if (windowWidth < reguralWidth + sideMargins) {
                    newMaxWidth = reguralWidth
                } else {
                    newMaxWidth = windowWidth - sideMargins
                }
            }

            const getMargin = (width) => {
                let margin = (effectiveContentWidth - width) / 2
                return Math.min(margin, -12) + offset
            }

            const width = Math.min(windowWidth, newMaxWidth)
            const margin = getMargin(width)

            $el.css('margin-left',  margin + 'px')
            $el.css('margin-right', margin + 'px')
        }

        adjustMargins()

        $(window).resize(adjustMargins)
    }
})
