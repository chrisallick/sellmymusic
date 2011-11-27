$(document).ready( function() {
	
	$(".add-track").each( function(index,value) {
		$(this).click( function(event){
			event.preventDefault();
			$(this).parent().append('<input class="track" type="text">');
		});
	});

	$("#add-side").click( function(event) {
		event.preventDefault();
		var el = $('<div/>', {
		}).appendTo('#sides');
		el.append("<h3>Side:</h3>");
		el.append('<input class="side" type="text" />');
		el.append('<h3>Tracks: (<a class="add-track" href="#">add</a>)</h3>');
		el.append('<input class="track" type="text" />');
		
		$(".add-track").each( function(index,value) {
			$(this).click( function(event){
				event.preventDefault();
				$(this).parent().append('<input class="track" type="text">');
			});
		});
	});

})