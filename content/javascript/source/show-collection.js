$(function () {
    var $collection = $('#collection');
    var $trigger = $('#collection-trigger');

    $trigger.show();
    $collection.hide();

    $trigger.find('a').click(function (event) {
        event.preventDefault();

        var el = document.documentElement;
        var x = el.scrollLeft;
        var yStart = el.scrollTop;

        // don't scroll past the trigger
        var trigger = $trigger[0];
        var triggerBox = trigger.getBoundingClientRect();
        var yMax = yStart + triggerBox.top;

        $trigger.hide();

        $collection.fadeIn({
            duration: 300,
            progress: function (_, progress) {
                var yEnd = Math.min(yMax, el.scrollHeight - el.clientHeight);
                window.scrollTo(x, yStart + progress * (yEnd - yStart));
            }
        });
    });
});
