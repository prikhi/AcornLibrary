function lookup(isbn) {
    $.getJSON("/lookup/", { isbn: isbn },
        function(json) {
            $("#id_title").val(json['title']);
    });
}
function addClickHandler() {
    $("#get_info").click(function(){ lookup($("#id_isbn").val()) });
}
$(document).ready(addClickHandler);
