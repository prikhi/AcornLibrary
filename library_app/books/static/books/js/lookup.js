function lookup(isbn) {
    $('#spinner').fadeIn('fast');
    $.getJSON("/lookup/", { isbn: isbn },
        function(json) {
        if (json['success'] == true) { 
                $("#id_title").val(json['title']);
                $("#id_author").val(json['author']);
                $("#id_dewey_decimal").val(json['dewey_decimal']);
                $('#spinner').fadeOut('fast');
        } else {
            $('#spinner').fadeOut('fast', function(){
                alert("ISBN not found");
            });            
        }
        
    });
}
function addClickHandler() {
    $("#get_info").click(function(){ lookup($("#id_isbn").val()) });
}

$(document).ready(function() {
    addClickHandler();
});
