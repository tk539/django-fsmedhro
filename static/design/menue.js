$('.hamburger').on('click', function(){
	if($('nav').hasClass('open')){
		$('nav').removeClass('open');
	} else{
		$('nav').addClass('open');
	}
});