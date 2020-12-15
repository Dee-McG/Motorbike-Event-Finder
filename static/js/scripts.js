$(document).ready(function(){
    // JS to make the navigation items expand out from the right side on smaller devices where it is collapsed.
    $('.sidenav').sidenav({edge: "right"});
    // Select options
    $('select').formSelect();
    // Date picker 
    $('.datepicker').datepicker({
        format: "dd mmmm, yyyy",
        yearRange: 3,
        showClearBtn: true,
        i18n: {
            done: "Select"
        }
    });
});