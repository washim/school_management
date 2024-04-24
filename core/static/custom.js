(function ($) {
    'use strict'
    $('input[type=text], input[type=file], input[type=number], select, textarea').addClass('form-control');
    $('textarea').attr('rows', 2);
    $('.datepicker').attr("type", "date").attr("min", "2023-01-01").attr("max", "2030-12-31");
})(jQuery)