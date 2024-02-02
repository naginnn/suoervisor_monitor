from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request, Response
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPAuthorizationCredentials
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from pkg.auth import check_token, check_usr
from settings.rpc import get_rpc_client

templates = Jinja2Templates(directory="templates")

auth = APIRouter(tags=["auth"])


@auth.get("/auth", response_class=HTMLResponse)
async def authtorization(request: Request):
    return templates.TemplateResponse(
        request=request, name="auth.html"
    )


@auth.get("/token")
async def get_token(response: Response,
                    basic_auth: HTTPAuthorizationCredentials = Depends(HTTPBasic(auto_error=False))):
    token = check_usr(basic_auth)
    if token is None:
        raise HTTPException(status_code=302, detail="Not authenticated", headers={"Location": "/auth"})
    response.set_cookie(key="token", value="ZAEBISTOKEN")
    return dict(token="ZAEBISTOKEN")



signals = APIRouter(tags=["signals"], dependencies=[Depends(check_token)], )


@signals.get("/apps", response_class=HTMLResponse)
async def apps(request: Request):
    return templates.TemplateResponse(
        request=request, name="apps.html"
    )


# ajax
@signals.get("/apps/info")
async def apps_info(client: Annotated[object, Depends(get_rpc_client)]):
    data, err = client.info.get_processes_info()
    if err:
        data = dict(apps=[], state="FATAL, PID NOT FOUND")
    return data


@signals.get("/supervisor_settings", response_class=HTMLResponse)
async def supervisor_settings(request: Request, client: Annotated[object, Depends(get_rpc_client)]):
    data, err = client.info.get_all_config()
    if err:
        data = dict(config=[], names=[], pid="Нет данных")

    return templates.TemplateResponse(
        request=request, name="supervisor.html", context=data
    )


@signals.get("/apps/{app}", response_class=HTMLResponse)
async def apps(request: Request, app: str, client: Annotated[object, Depends(get_rpc_client)]):
    data, err = client.info.get_process_info(app)
    if err:
        data = dict()
    return templates.TemplateResponse(
        request=request, name="app.html", context=data
    )


@signals.get("/apps/{app}/{log_type}", response_class=HTMLResponse)
async def app_logs(request: Request, app: str, log_type: str, client: Annotated[object, Depends(get_rpc_client)]):
    if log_type == 'stdout_logfile':
        data, err = client.info.tail_process_stdout_log(app)
    elif log_type == 'stderr_logfile':
        data, err = client.info.tail_process_stderr_log(app)
    if err:
        data = dict(name=app, log="Empty")
    return templates.TemplateResponse(
        request=request, name="logs.html", context=data
    )


control = APIRouter(tags=["control"], dependencies=[Depends(check_token)], )


@control.post("/supervisor/control/{cmd}")
async def control_supervisor(request: Request, cmd: str, response: Response,
                             client: Annotated[object, Depends(get_rpc_client)]):
    res, err = client.internal.run_command(cmd)
    if err:
        response.status_code = 500


@control.post("/apps/control/{command}", status_code=201)
async def control_apps(command: str, response: Response, client: Annotated[object, Depends(get_rpc_client)]):
    res, err = client.external.run_all_command(command)
    if err:
        response.status_code = 500
    else:
        response.status_code = 200


@control.post("/apps/{app}/control/{command}", status_code=201)
async def control_app(response: Response, app: str, command: str, client: Annotated[object, Depends(get_rpc_client)]):
    # server = ServerProxy('http://localhost:9001/RPC2')
    if command == "stop":
        res, err = client.external.stop_process(command)
    elif command == "start":
        res, err = client.external.start_process(command)
    elif command == "restart":
        res, err = client.external.restart_process(command)
    if err:
        response.status_code = 500
    else:
        response.status_code = 200
