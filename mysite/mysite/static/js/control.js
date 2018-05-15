$("#keywords").click(function(e) {
        e.preventDefault();
        $('.data-leftnav').removeClass('.data-leftnav-active');
        $(this).addClass('.data-leftnav-active');
    });