/* -- jQuery stuff for dynamic page handling / carabana.cz */

var x = 0, x2 = 0, y = 0, y2 = 0, width, options, ofcaClicked = false

function updateAnimation()
{
    // move sheep and related objects in the direction of mouse cursor
    
    delta = 0;
    if (width < 800) delta = -90;

    xOfca = Math.min(x * 0.03, 20);
    yOfca = (y >= 0) ? Math.min(y * 0.06, 40) : -100;
    $('#carabana-logo #ofca').animate({ left: (xOfca - 10) + 'px', top: (yOfca - 30) + 'px'}, options);

    xTube = Math.min(x * 0.02, 15);
    yTube = (y >= 0) ? Math.min(y * 0.05, 33) : -95;
    $('#carabana-logo #tube').animate({ left: (xTube + 385 + delta) + 'px', top: yTube + 'px'}, options);

    xLandscape = Math.min(x * 0.015, 10);
    yLandscape = (y >= 0) ? Math.min(y * 0.03, 20) : -120;
    $('#carabana-logo #city').animate({ left: (xLandscape + 220 + delta) + 'px', top: (yLandscape + 1) + 'px'}, options);
    $('#carabana-logo #village').animate({ left: (xLandscape + 458 + delta) + 'px', top: (yLandscape + 82) + 'px'}, options);

    xSun = Math.min(x * 0.01, 7);
    ySun = (y >= 0) ? Math.min(y * 0.02, 13) : -110;
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
        x2 = Math.max(event.pageX - 300, 0);
        y2 = Math.max(event.pageY - 100, 0);
        if (!ofcaClicked)
        {
            // user has not yet clicked on the objects, move them
            x = x2; y = y2;
            width = $('#wrapper').width();
            
            updateAnimation();
        }
    });
    

    $('#carabana-logo #ofca').click(function(e) {
    
        width = $('#wrapper').width();
        e.preventDefault();
        options = { duration: 600, queue: false };

        if (!ofcaClicked)
        {
            // first click, move sheep to the page top and fix it there
            y = -1;
            ofcaClicked = true;
            $('#carabana-logo #light').animate({ top: '-145px' }, options);
        }
        else
        {
            // second click, get the sheep back down
            x = x2; y = y2;
            window.setTimeout(function() { ofcaClicked = false; }, 700);
            $('#carabana-logo #light').animate({ top: '0px' }, options);
        }

        updateAnimation();
    });


    $(window).resize(function() {

        width = $('#wrapper').width();
        updateAnimation();

    });


    // change cz / en impress text regularly
    window.setInterval(function() {

        if ($('.impress .cz').is(":visible"))
        {
            $('.impress .cz').slideUp('slow');
            $('.impress .en').slideDown('slow');
        }
        else
        {
            $('.impress .en').slideUp('slow');
            $('.impress .cz').slideDown('slow');
        }

    }, 5000);


    // AJAX loader for more articles on home page (django endless pagination plugin)
    $(document).on("click", "a.endless_more", function() {
        var container = $(this).closest(".endless_container");
        var loading = container.find(".endless_loading");
        $(this).hide();
        loading.show();
        var data = "querystring_key=" + $(this).attr("rel").split(" ")[0];
        $.get($(this).attr("href"), data, function(data) {
            container.before(data);
            container.remove();
            $("article .column").fadeTo(500, 1);
        });
        return false;
    });


    // page ready: fade in the sheep and related objects    
    $('#carabana-logo').hide().fadeTo(1000, 1);
    
});

