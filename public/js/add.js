postAlbumData = function( album ) {
	$.ajax({
		url: "/add",
		type: 'POST',
		data: { 'album': JSON.stringify(album) },
		dataType: 'json',
		beforeSend: function() {
			$("#album-data").slideUp('fast');
			$("#loading").show();
		},
		success: function(data) {
			$("#loading").hide();
			submitFiles();
		},
		error: function(data){
			$("#loading").hide();
		}
	});
}

deleteAlbum = function( catnum ) {
	$.ajax({
		url: "/delete",
		type: 'POST',
		data: { 'remove': catnum },
		dataType: 'json',
		beforeSend: function() {
			$("#album-data").slideUp('fast');
			$("#loading").show();
		},
		success: function(data) {
			$("#loading").hide();
		},
		error: function(data){
			$("#loading").hide();
		}
	});
}

crunchAlbumData = function( data ) {
	error = false;

	var album = {};
	$.each(data, function() {
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

	var fileInput = document.getElementById('files');
	if( fileInput.files['length'] < 1 || fileInput.files['length'] > 5 ) {
		alert("You must have between 1 and 5 files.");
		error = true;
	} else {
		var files = Array();
		for( j = 0, len = fileInput.files['length']; j < len; j++ ) {
			f = fileInput.files[j];
			files.push(album['catnum']+'.'+f.name);
		}
		album['artwork'] = files;
	}

	if( !error ) {
		postAlbumData( album );
	}
}

submitFiles = function() {
	var fileInput = document.getElementById('files');
	if( fileInput.files['length'] == 0 ) {
		alert("no files");
	} else {
		for( j = 0, len = fileInput.files['length']; j < len; j++ ) {
			f = fileInput.files[j];
			var xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4) {
                    try { var resp = JSON.parse( xhr.responseText ); } catch(e) {}
                    if( resp && resp["result"] == "success" ) {
                        console.log( resp );
                    }
                }
            };
            onProgressHandler = function(event) {
                var percent = event.loaded/event.total;
                if( percent == 1 ) {}
            };
            onLoadStartHandler = function(event) {
                console.log( "started!" );
            };
            xhr.upload.addEventListener("progress", onProgressHandler, false);
            xhr.upload.addEventListener("onloadstart", onLoadStartHandler, false);
			xhr.open('POST', '/addfile', true );
			xhr.setRequestHeader("X-Filename", f.name);	
			xhr.setRequestHeader("Content-Type", "application/octet-stream");
			xhr.send( f );
		}
	}
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
	});

	$('form').submit(function(event) {
		event.preventDefault();
		crunchAlbumData( $(this).serializeArray() );
	});

	$("#delete").click(function(event){
		event.preventDefault();
		deleteAlbum( $("#catnum").val() );
	})
})