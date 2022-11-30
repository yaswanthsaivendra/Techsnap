var owl = $('.cards-slider').owlCarousel({
    loop: true,
    responsiveClass: true,
    autoplayTimeout: 4000,
    smartSpeed: 400,
    nav: true,
    margin: 0,
    center: true,
    navText: [' < ', ' > '],
    responsive: {
        0: {
            items: 1,
        },
        600: {
            items: 3
        },
        1200: {
            items: 3
        }
    }
  });

  /****************************/

  jQuery(document.documentElement).keydown(function (event) {

    if (event.keyCode == 37) {
      owl.trigger('prev.owl.carousel', [400]);
    } else if (event.keyCode == 39) {
        owl.trigger('next.owl.carousel', [400]);
    }

  });