window.auth = () => {
    return () => {
        const usr = $('#usr').val();
        const pwd = $('#pwd').val();
        const data64 = btoa(`${usr}:${pwd}`);
        $.ajax({
            url: '/token',         /* Куда пойдет запрос */
            method: 'get',             /* Метод передачи (post или get) */
            dataType: 'json',
            headers: {"Authorization": "Basic " + data64},
            success: function (data) {   /* функция которая будет выполнена после успешного запроса.  */
                console.log(data);
                window.location.href = "/apps";
            },
            302: function (response) {
                // window.location.href = "/auth";
            },
        });
    }
}

(function ($) {
    $('#sign-in').click(auth());
})($);