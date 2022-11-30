$('.generate-qr-code').on('click', function() {

    // Clear Previous QR Code
    $('#qrcode').empty();

    // Set Size to Match User Input
    $('#qrcode').css({
        'width': $('.qr-size').val(),
        'height': $('.qr-size').val()
    })

    // Generate and Output QR Code
    $('#qrcode').qrcode({
        width: $('.qr-size').val(),
        height: $('.qr-size').val(),
        text: $('.qr-url').val()
    });
    document.getElementById('download').style.display = 'block';
});

function downloadQR() {
    html2canvas(document.querySelector("#qrcode")).then(canvas => {
        //document.body.appendChild(canvas);
        var img = canvas.toDataURL("image/png");
        var link = document.createElement('a');
        link.href = img;
        link.download = 'qrcode.png';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });

}