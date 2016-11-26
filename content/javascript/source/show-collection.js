$(function () {
    var $collection = $('#collection');
    var $trigger = $('#collection-trigger');

    $trigger.show();
    $collection.hide();

    $trigger.find('a').click(function (event) {
        event.preventDefault();

        $trigger.hide();

        $window = $(window);
        var x = $window.scrollLeft();
        var yStart = $window.scrollTop();
        var yDelta = 0;

        $collection.fadeIn({
            duration: 300,
            progress: function (_, progress) {
                yDelta = yDelta || (document.body.scrollHeight - $window.height() - yStart);
                window.scrollTo(x, yStart + progress * yDelta);
            }
        });
    });
});
