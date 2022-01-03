$(function () {
    var $web2 = $('#web2');
    var $trigger = $('#web2-trigger');

    $trigger.removeClass('hidden');
    $web2.hide();

    $trigger.find('a').click(function (event) {
        event.preventDefault();
        $trigger.hide();
        $web2.fadeIn(500);
    });
});
