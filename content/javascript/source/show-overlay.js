// mobile :hover equivalent
//
// If there's any JS handler on the element, the `:hover` behaviour
// is provided for free by the browser, but it's sticky — doesn't
// disappear on `touchend`. Therefore I explicitily add and remove
// classes to control presentation both on touch start and end.
$(function () {
    const start = 'touchstart'
    const end = 'touchend'

    $('.overlay').on(start, function () {
        $(this).removeClass(end).addClass(start)
    }).on(end, function () {
        $(this).removeClass(start).addClass(end)
    })
})
