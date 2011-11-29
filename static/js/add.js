submitAlbumData = function( data ) {
	var album = {};
	$.each(data, function() {
		//console.log(this.name + ", " + this.value);
		album[this.name] = this.value;
	});

	album['tracks'] = Array();
	$.each( $("#sides div"), function() {
		var side = {};
		//console.log( $('.side',this).val() );
		side['name'] = $('.side',this).val();
		side['tracks'] = Array();
		$.each( $('.track', this), function() {
			//console.log( $(this).val() );
			side['tracks'].push( $(this).val() );
		});
		album['tracks'].push( side );
	});
	//console.log( album );
	$.ajax({
		url: "/add",
		type: 'POST',
		data: { 'album': JSON.stringify(album) },
		dataType: 'json',
		beforeSend: function() {
			$("#add-album").slideUp('fast');
			$("#loading-gif").css("display", "inline");
		},
		success: function(data) {
			$("#loading-gif").css("display", "none");
			console.log( data.msg );
		},
		error: function(data){
			$("#loading-gif").css("display", "none");
		}
	});
}

submitFiles = function() {
	var fileInput = document.getElementById('files');
	if( fileInput.files['length'] == 0 ) {
		alert("no files");
	} else {
		for( j = 0, len = fileInput.files['length']; j < len; j++ ) {
			f = fileInput.files[j];
			var xhr = new XMLHttpRequest();
			xhr.onload = onloadHandler( f.name );
			xhr.open('POST', '/upload', true );
			xhr.setRequestHeader("X-File-Name", f.name);	
			xhr.setRequestHeader("Content-Type", "application/octet-stream");
			xhr.send( f );
		}
	}
}

onloadHandler = function( event, filename ) {
	console.log( filename );
}

$(document).ready( function() {
	
	$(".add-track").each( function(index,value) {
		$(this).click( function(event){
			event.preventDefault();
			$(this).closest('div').append('<input class="track" type="text" />');
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
				$(this).closest('div').append('<input class="track" type="text" />');
			});
		});
	});
	
	$("#submit").click( function( event ) {
		event.preventDefault();
		$("form").submit();
		//submitFiles();
	});

	$('form').submit(function(event) {
		event.preventDefault();
		submitAlbumData( $(this).serializeArray() );
	});
})