window.controlProcesses = (command) => {

    return () => {
        // $('#loading').css("display", "");
    $.ajax({
        url: window.location.href + '/control/' + command,         /* Куда пойдет запрос */
        method: 'post',             /* Метод передачи (post или get) */
        dataType: 'json',          /* Тип данных в ответе (xml, json, script, html). */
        success: function (data) {   /* функция которая будет выполнена после успешного запроса.  */
            console.log(data);
            window.location.reload();
            // $('#loading').css("display", "none");
        },
        302: function (response) {
                window.location.href = "/auth";
            },
    });
}}

(function ($) {
    $('#start-app-btn').click(controlProcesses('start'));
    $('#stop-app-btn').click(controlProcesses('stop'));
})($);