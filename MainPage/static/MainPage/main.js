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


$("about_header").click(function () {
    alert("HIIIII");

    $about_header = $(this);
    //getting the next element
    $about_content = $about_header.next();
    //open up the content needed - toggle the slide- if visible, slide up, if not slidedown.
    $about_content.slideToggle(500, function () {
        //execute this after slideToggle is done
        //change text of header based on visibility of content div
        $about_header.text(function () {
            //change text based on condition
            return $about_content.is(":visible") ? "Collapse" : "Expand";
        });
    })(jQuery);

});