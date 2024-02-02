window.controlSupervisor = (command) => {
    const token = localStorage.getItem('token');
    return () => {
        $('#loading').css("display", "");
        $.ajax({
            url: '/supervisor/control/' + command,         /* Куда пойдет запрос */
            method: 'post',             /* Метод передачи (post или get) */
            dataType: 'json',          /* Тип данных в ответе (xml, json, script, html). */
            success: function (data) {   /* функция которая будет выполнена после успешного запроса.  */
                $('#loading').css("display", "none");
                location.reload();

            },
            302: function (response) {
                window.location.href = "/auth";
            },
            error: ()=> {
                $('#loading').css("display", "none");
            }
        });
    }
}

(function ($) {
    $('#shutdown').click(controlSupervisor('shutdown'));
    $('#restart').click(controlSupervisor('restart'));
    $('#clear-log').click(controlSupervisor('clear_log'));
    $('#reload-config').click(controlSupervisor('reload_config'));
    $('#shutdown-and-apply-config').click(controlSupervisor('shutdown_and_apply_config'));
})($);