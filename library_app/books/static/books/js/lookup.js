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
                var selectize_subjects = $("#id_subjects")[0].selectize;
                for (var i=0; i<json.subjects.length; i++) {
                    selectize_subjects.addOption({
                        text: json.subjects[i],
                        value: json.subjects[i]
                    });
                    selectize_subjects.addItem(json.subjects[i])
                }
                $("#id_dewey_decimal").val(json['dewey_decimal']);
                $("#id_description").val(json['description']);
                $('#spinner').fadeOut('fast');
        } else {
            $('#spinner').fadeOut('fast', function(){
                alert("ISBN not found");
            });            
        }
        
    });
    $("#submit").focus();
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
				    create: true 
				});
				
	$("#id_subjects").selectize({
					plugins: ['remove_button'],
					delimiter: '%',
				    persist: false,
				    create: true 
				});
				
	$("#get_info").appendTo($("#id_isbn").parent());
	$("#id_isbn").focus();
	
	$("#id_isbn").keypress(function(event){
        if(event.which == 13){
            event.preventDefault();
            $("#get_info").click();
        }
    });
    
    $("#id_is_ebook_only").change(function(){
        if(this.checked) {
            $("#id_owner").val("");
            $("#id_location").val("");
        }
    });
    
});
