$(function () {
    var $web2 = $('#web2');
    var $trigger = $('#web2-trigger');
    var cls = 'hidden';

    $web2.addClass(cls);

    $trigger.click(function (event) {
        event.preventDefault();
        $web2.toggleClass(cls);
    });
});
