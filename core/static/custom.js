(function ($) {
    'use strict'
    $('input[type=text], input[type=file], input[type=number], select, textarea').addClass('form-control');
    $('textarea').attr('rows', 2);
    $('select').select2();
    $('.datepicker').attr("type", "date").attr("min", "1950-01-01").attr("max", "2030-12-31");
    $('.printout').click(function() {
        $('.printerdiv').html('<iframe src="'+$(this).data("print-target-page")+'" onload="this.contentWindow.print();"></iframe>');
    });
})(jQuery)