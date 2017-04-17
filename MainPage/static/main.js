$(document).ready(function() {
    (function ($) {

        $('.tab ul.tabs').addClass('active').find('> li:eq(0)').addClass('current');

        $('.tab ul.tabs li a').click(function (g) {
            var tab = $(this).closest('.tab'),
                index = $(this).closest('li').index();

            tab.find('ul.tabs > li').removeClass('current');
            $(this).closest('li').addClass('current');

            tab.find('.tab_content').find('div.tabs_item').not('div.tabs_item:eq(' + index + ')').slideUp();
            tab.find('.tab_content').find('div.tabs_item:eq(' + index + ')').slideDown();

            g.preventDefault();
        } );
    })(jQuery);





});

$(window).load(function() {
    $('#about-content').hide();
    $('#algo-content').hide();
    $('#ref-content').hide();
    $('#mi-content').hide();

    $('#about-header').on('click', function(event) {

        if ($('#about-content').is(':hidden')) {
            $('#about-header').html('<h5>&#8743; &nbsp; About Sentiment Analysis</h5>');
        }
        if ($('#about-content').is(':visible')){
            $('#about-header').html('<h5>&#8744; &nbsp; About Sentiment Analysis</h5>');
        }
        $('#about-content').toggle('show');
    });

    $('#algo-header').on('click', function(event) {

        if ($('#algo-content').is(':hidden')) {
            $('#algo-header').html('<h5>&#8743; &nbsp; Algorithm</h5>');
        }
        if ($('#algo-content').is(':visible')){
            $('#algo-header').html('<h5>&#8744; &nbsp; Algorithm</h5>');
        }
        $('#algo-content').toggle('show');
    });

    $('#ref-header').on('click', function(event) {
        if ($('#ref-content').is(':hidden')) {
            $('#ref-header').html('<h5>&#8743; &nbsp; References</h5>');
        }
        if ($('#ref-content').is(':visible')){
            $('#ref-header').html('<h5>&#8744; &nbsp; References</h5>');
        }
        $('#ref-content').toggle('show');
    });

    $('#mi-header').on('click', function(event) {
        if ($('#mi-content').is(':hidden')) {
            $('#mi-header').html('<h5>&#8743; &nbsp; More information</h5>');
        }
        if ($('#mi-content').is(':visible')){
            $('#mi-header').html('<h5>&#8744; &nbsp; More Information</h5>');
        }
        $('#mi-content').toggle('show');
    });


    $('.directions-content').hide();
    $('.directions-header').on('click', function(event) {
        $('.directions-content').toggle('show');
    });

    $('.stats-content').hide();
    $('.stats-header').on('click', function(event) {
        $('.stats-content').toggle('show');
    });

});


// $about_header = $(this);
//         //getting the next element
//         $about_content = $about_header.next();
//         //open up the content needed - toggle the slide- if visible, slide up, if not slidedown.
//         $about_content.slideToggle(500, function () {
//             //execute this after slideToggle is done
//             //change text of header based on visibility of content div
//             $about_header.text(function () {
//                 //change text based on condition
//                 return $about_content.is(":visible") ? "Collapse" : "Expand";
//             });
//         })(jQuery);
