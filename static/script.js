function fORp(id) {
    let opid = id + '1';
    opid = document.getElementById(opid);
    document.getElementById(id).style.opacity=2;
    opid.style.display='block';
    
    if (id == "freecourses") {
        document.getElementById('paidcourses').style.opacity=0.5;
        document.getElementById('paidcourses1').style.display = 'none';
        document.getElementById('paid-courses').style.display = 'none';
        document.getElementById('free-courses').style.display = 'block';
    }
    else {
        document.getElementById('freecourses').style.opacity=0.5;
        document.getElementById('freecourses1').style.display = 'none';
        document.getElementById('free-courses').style.display = 'none';
        document.getElementById('paid-courses').style.display = 'block';
    }
}
$('.tab-link').on('click', function() {
    // Switch the class on the previously active div to make it hidden
    $('.active-demo').removeClass('active-demo').addClass('inactive');
    // Switch the class on the new active div to show it
    var selectorForActiveDemo = $(this).attr('href');
    $(selectorForActiveDemo).removeClass('inactive').addClass('active-demo');
});
$(document).ready(function () {
      $(".owl-carousel").owlCarousel({
          items:1,
          loop:true,
          nav:false,
          dots:true,
          autoplay:true,
          autoplaySpeed:1000,
          smartSpeed:1000
      });
});

// $('.freeORpaid').on("click", '.nav-link', function () {
//     let id = $(this).attr("data-sid");
    
// })
  


