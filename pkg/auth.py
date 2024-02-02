import asyncio
from typing import Annotated, Optional

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBearer, HTTPAuthorizationCredentials
from starlette.responses import RedirectResponse
from fastapi import Request, Response


# from src.auth.utils import check_adapter
def check_token(request: Request):
    token = request.cookies.get("token")
    if token == "ZAEBISTOKEN":
        return True
    else:
        raise HTTPException(status_code=302, detail="Not authenticated", headers={"Location": "/auth"})


#### check in ipa group or hardcoded logins
def check_usr(basic_auth: HTTPAuthorizationCredentials):
    print(basic_auth)
    return True


