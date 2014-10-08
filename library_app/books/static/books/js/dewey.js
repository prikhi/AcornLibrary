$(document).ready(function() {
$('#dewey_tree').jstree().on("select_node.jstree", function (e, data) {
           document.location = data.instance.get_node(data.node, true).children('a').attr('href');
    });;



});
