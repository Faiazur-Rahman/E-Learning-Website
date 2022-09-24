$(document).on("scroll", function(){

    if ($(document).scrollTop() > 80){
        $(".primary-nav").addClass("shrink");
    } else {
        $(".primary-nav").removeClass("shrink");
    }
  var Logo = document.getElementById("Logo");
  if (document.body.scrollTop > 5 || document.documentElement.scrollTop > 5) {
    Logo.style.height = '40px';
    Logo.style.width = '100px';
    document.getElementById("profile-logo").style.height = '30px';
    document.getElementById("profile-logo").style.width = '30px';
    document.getElementById("pr-lgoli").style.paddingTop = '5px';
    //Logo.style.paddingLeft='10px';
  } else {
    Logo.style.height = '60px';
    Logo.style.width = '120px';
    document.getElementById("profile-logo").style.height = '100%';
    document.getElementById("profile-logo").style.width = '100%';
    document.getElementById("pr-lgoli").style.paddingTop = '10px';
    //Logo.style.paddingLeft='10px';
  }

  });