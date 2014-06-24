function lookup(isbn) {
    $('#spinner').fadeIn('fast');
    $.getJSON("/lookup/", { isbn: isbn },
        function(json) {
        if (json['success'] == true) { 
                $("#id_title").val(json['title']);
                var selectize_authors = $("#id_authors")[0].selectize;
                for (var i=0; i<json.authors.length; i++) {
                    selectize_authors.addOption({
                        text: json.authors[i],
                        value: json.authors[i]
                    });
                    selectize_authors.addItem(json.authors[i])
                }
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
    $("#id_authors").selectize({
					plugins: ['remove_button'],
					delimiter: '%',
				    persist: false,
				    create: true /*function(input) {
				        return {
				            value: input,
				            text: input
				        }
				    }*/
				});
});
