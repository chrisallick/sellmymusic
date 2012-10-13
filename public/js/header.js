$(document).ready(function(){
	$("#gocontact").click(function(event){
		event.preventDefault();
		$("#contactinfo").slideToggle();
		$(this).toggleClass("on");
	});
});