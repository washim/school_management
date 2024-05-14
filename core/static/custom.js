(function ($) {
    'use strict'
    $('input[type=text], input[type=file], input[type=number], select, textarea').addClass('form-control');
    $('textarea').attr('rows', 2);
    $('select').select2();
    $('.datepicker').attr("type", "date").attr("min", "1950-01-01").attr("max", "2030-12-31");
    $('.printout').click(function() {
        $('.printerdiv').html('<iframe src="'+$(this).data("print-target-page")+'" onload="this.contentWindow.print();"></iframe>');
    });

    $('#id_tuition_fee_paid, #id_admission_fee_paid, #id_learning_material_fee_paid, #id_hostel_fee_paid, #id_others_fee_paid').on('change',function(){
        autocalculate();
    });

    $('#id_tuition_fee_total, #id_admission_fee_total, #id_learning_material_fee_total, #id_hostel_fee_total, #id_others_fee_total').on('change',function(){
        autocalculate();
    });

    autocalculate();

    function autocalculate() {
        var tution_fee_total = $('#id_tuition_fee_total').val();
        var tution_fee_paid = $('#id_tuition_fee_paid').val();
        var tution_fee_due = tution_fee_total - tution_fee_paid;
        $('#id_tuition_fee_due').val(tution_fee_due);

        var admission_fee_total = $('#id_admission_fee_total').val();
        var admission_fee_paid = $('#id_admission_fee_paid').val();
        var admission_fee_due = admission_fee_total - admission_fee_paid;
        $('#id_admission_fee_due').val(admission_fee_due);

        var material_fee_total = $('#id_learning_material_fee_total').val();
        var material_fee_paid = $('#id_learning_material_fee_paid').val();
        var material_fee_due = material_fee_total - material_fee_paid;
        $('#id_learning_material_fee_due').val(material_fee_due);

        var hostel_fee_total = $('#id_hostel_fee_total').val();
        var hostel_fee_paid = $('#id_hostel_fee_paid').val();
        var hostel_fee_due = hostel_fee_total - hostel_fee_paid;
        $('#id_hostel_fee_due').val(hostel_fee_due);

        var others_fee_total = $('#id_others_fee_total').val();
        var others_fee_paid = $('#id_others_fee_paid').val();
        var others_fee_due = others_fee_total - others_fee_paid;
        $('#id_others_fee_due').val(others_fee_due);

        $('#total_paid').html(Number(tution_fee_paid)+Number(admission_fee_paid)+Number(material_fee_paid)+Number(hostel_fee_paid)+Number(others_fee_paid));
        $('#total_due').html(Number(tution_fee_due)+Number(admission_fee_due)+Number(material_fee_due)+Number(hostel_fee_due)+Number(others_fee_due));
    }
})(jQuery)