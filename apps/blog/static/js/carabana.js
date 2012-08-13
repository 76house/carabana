/* -- jQuery stuff for dynamic page handling / carabana.cz */

var x = 0, y = 0, width, options

function updateAnimation()
{
    delta = 0;
    if (width < 800) delta = -90;

    xOfca = Math.min(x * 0.03, 20);
    yOfca = Math.min(y * 0.06, 40);
    $('#carabana-logo #ofca').animate({ left: (xOfca - 10) + 'px', top: (yOfca - 30) + 'px'}, options);

    xTube = Math.min(x * 0.02, 15);
    yTube = Math.min(y * 0.05, 33);
    $('#carabana-logo #tube').animate({ left: (xTube + 385 + delta) + 'px', top: yTube + 'px'}, options);

    xLandscape = Math.min(x * 0.015, 10);
    yLandscape = Math.min(y * 0.03, 20);
    $('#carabana-logo #city').animate({ left: (xLandscape + 220 + delta) + 'px', top: (yLandscape + 1) + 'px'}, options);
    $('#carabana-logo #village').animate({ left: (xLandscape + 458 + delta) + 'px', top: (yLandscape + 82) + 'px'}, options);

    xSun = Math.min(x * 0.01, 7);
    ySun = Math.min(y * 0.02, 13);
    $('#carabana-logo #sun').animate({ left: (xSun + 515 + delta) + 'px', top: (ySun - 6) + 'px'}, options);

    rotateOfca = 'rotate(' + (Math.min(x * 0.008, 4) - 2) + 'deg)';
    rotateTube = 'rotate(' + Math.min(y * 0.005, 4) + 'deg)';
    $('#carabana-logo #ofca').css({ '-webkit-transform': rotateOfca, '-moz-transform': rotateOfca, '-o-transform': rotateOfca, '-ms-transform': rotateOfca });
    $('#carabana-logo #tube').css({ '-webkit-transform': rotateTube, '-moz-transform': rotateTube, '-o-transform': rotateTube, '-ms-transform': rotateTube });
    
    options = { duration: 0, queue: true };
}

$(document).ready(function()
{
    options = { duration: 100, queue: true };

    $("body").mousemove(function(event) {
        x = Math.max(event.pageX - 300, 0);
        y = Math.max(event.pageY - 100, 0);
        width = $('#wrapper').width();
        
        updateAnimation();
    });

    $(window).resize(function() {
        width = $('#wrapper').width();
        updateAnimation();
    });

});

