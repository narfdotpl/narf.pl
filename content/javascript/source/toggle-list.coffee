toggleList = ($list, $toggle) ->
    # choose action
    dataKey = 'is-expanded'
    hide = !!$toggle.data(dataKey)

    # prepare to toggle list items
    $items = $list.find('.hidden')
    getDelay = (i) ->
        50 * if hide
            $items.length - 1 - i
        else
            i

    # toggle list items
    methodName = if hide then 'fadeOut' else 'fadeIn'
    $items.each (i) ->
        $(@).delay(getDelay(i))[methodName]()

    # toggle toggle
    duration = 100
    $toggle.data(dataKey, !hide)
    $toggle.fadeOut duration, ->
        $toggle.html(if hide then '&hellip;' else '&#8593;')

    $toggle.delay(Math.max(duration, getDelay($items.length - 1))).fadeIn()


$ ->
    $('ul').each ->
        $list = $(@)

        # get toggle link
        $toggle = $list.find('.js-toggle a')

        # fail fast
        if $toggle.length == 0
            return

        # react to clicks
        $toggle.click ->
            toggleList($list, $toggle)
            no
