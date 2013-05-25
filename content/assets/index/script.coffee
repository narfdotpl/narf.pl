$ ->
    $('ul').each ->
        $list = $(@)

        # fail fast
        return if $list.find('.hidden').length is 0

        # create extra "buttons"
        $3dots = $list.find('.ellipsis')

        $up = $('<li><a href="#">&#8593;</a></li>')
            .hide().appendTo($list)

        bind = ($trigger, $replacement, fadeIn) ->
            $trigger.click ->
                methodName = if fadeIn then 'fadeIn' else 'fadeOut'
                $items = $list.find('.hidden')
                getDelay = (i) ->
                    50 * if fadeIn
                        i
                    else
                        $items.length - 1 - i
                $items.each (i) ->
                    $(@).delay(getDelay(i))[methodName]()

                $trigger.fadeOut -> $replacement.fadeIn()

                no

        # react to clicks
        for [$trigger, $replacement, fadeIn] in [
            [$3dots, $up, yes],
            [$up, $3dots, no]
        ]
            bind($trigger, $replacement, fadeIn)
