from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from src.form import LoginForm
from src.user_dao import UserDAO
from src.constants import TEMPLATES_DIR, LOGIN_SUCCESS_MSG, LOGIN_ERROR_MSG, LOGIN_INCORRECT_MSG


default_route = APIRouter()
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# ----------------
# -- Home  Page --
# ----------------
@default_route.get("/", response_class=HTMLResponse)
def index(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("index.html", context)


# ----------------
# -- Login Page --
# ----------------
@default_route.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("login.html", context)


@default_route.post("/login")
async def login_post(request: Request, response_class=HTMLResponse):
    form = LoginForm(request)
    
    await form.load_data()
    
    if await form.is_valid():
        try:
            response = RedirectResponse("/private", status.HTTP_302_FOUND)
            userdao = UserDAO()
            user = userdao.authenticate_user(form.username, form.password)
            
            if not user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=LOGIN_INCORRECT_MSG)
            form.__dict__.update(msg=LOGIN_SUCCESS_MSG)
            
            # Redirect to portal!
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append(LOGIN_ERROR_MSG)
            return templates.TemplateResponse("login.html", form.__dict__)
        
    # In case we have an invalid credential or password
    return templates.TemplateResponse("login.html", form.__dict__)


# ----------------
# -- Private --
# ----------------
@default_route.get("/private", response_class=HTMLResponse)
def private(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("private.html", context)