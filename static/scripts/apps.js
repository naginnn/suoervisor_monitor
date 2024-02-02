window.controlProcesses = (command) => {
    const token = localStorage.getItem('token');
    return () => {
        $('#loading').css("display", "");
        $.ajax({
            url: '/apps/control/' + command,         /* Куда пойдет запрос */
            method: 'post',             /* Метод передачи (post или get) */
            dataType: 'json',          /* Тип данных в ответе (xml, json, script, html). */
            success: function (data) {   /* функция которая будет выполнена после успешного запроса.  */
                $('#loading').css("display", "none");

            },
            302: function (response) {
                window.location.href = "/auth";
            },
            error: (response)=> {
                alert("Команды не доступны");
                window.location.reload();
                $('#loading').css("display", "none");
            },

        });
    }
}

window.control = () => {
    return () => {
        window.location.replace("/supervisor_settings" );
    }

}
const updateAppsState = () => {
    $.ajax({
        url: '/apps/info',         /* Куда пойдет запрос */
        method: 'get',             /* Метод передачи (post или get) */
        dataType: 'json',          /* Тип данных в ответе (xml, json, script, html). */
        success: function (data) {   /* функция которая будет выполнена после успешного запроса.  */
            $('#spr_state').text("supervisord:" + data.state);
            let apps = data.apps
            $('#apps-body').empty();
            for (key in apps) {
                var row = $('<tr>');
                var hr = $('<a>').attr("href", document.URL + "/" + apps[key]["name"]);
                hr.attr("class", "nav-link").text(apps[key]["name"]);
                row.append($('<td>').html(hr));
                row.append($('<td>').html(apps[key]["statename"]));
                row.append($('<td>').html(apps[key]["description"]));
                $('#apps-body').append(row);
            }
        }
    });
}

(function ($) {

    $('#start-all-apps-btn').click(controlProcesses('start_all'));
    $('#stop-all-apps-btn').click(controlProcesses('stop_all'));
    $('#restart-all-apps-btn').click(controlProcesses('restart_all'));
    $('#supervisor-settings').click(control());
    // $('#supervisor-settings').click(controlProcesses('restart_all'));

    updateAppsState();
    setInterval(updateAppsState, 2000);
})($);


//<p style="color: #c2880b;" className="my-0"><input style="color: #c2880b;" className="my-1" value="{{key}}"/></p>-->
//<p style="color: #000000;" class="my-0"><input style="color: #000000;" class="my-1" value="{{value}}"/></p>-->