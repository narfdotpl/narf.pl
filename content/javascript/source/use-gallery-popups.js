$(function () {
    $('.gallery').each(function () {
        $(this).magnificPopup({
            delegate: 'a',
            type: 'image',
            gallery: {
                enabled: true,
                tCounter: ''  // don't show counter
            }
        });
    });
});
