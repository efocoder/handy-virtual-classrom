$(document).ready(function () {
    $('.start_date').datepicker({
        format: "yyyy-mm-dd",
    });
    $('.time_start').timepicker({
        twelveHour: false
    });
    $('.time_end').timepicker({
       twelveHour: false
    });
    $(".dropdown-trigger").dropdown();
    $(".dropdown-trigger-main").dropdown();
    $('.sidenav').sidenav();
    $('.modal').modal();
    $('.slider').slider();



    M.updateTextFields();
});