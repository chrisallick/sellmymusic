$(document).ready( function() {
	$(".album-artwork .thumbs .thumb").each( function(index, value) {
		if( index==0 ) {
			$(this).toggleClass("selected");
		}
		$(this).click( function(event) {
			if( !$(this).hasClass("selected") ) {
				$(this).siblings(".selected").toggleClass("selected");
				$(this).toggleClass("selected");

				$(this).parent().siblings(".large").attr("src", $(this).attr("src") );
			}
		});
	});
})