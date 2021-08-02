import uvicorn
from fastapi import FastAPI, Request, status, Form, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import Optional
from tools import htmlgen
from dotenv import load_dotenv
from deta import Deta
import os
import requests
import base64
import json
import sentry_sdk


load_dotenv()

app = FastAPI()
deta = Deta(os.getenv("DETA_TOKEN"))
tools = deta.Base("whatdevsneed-posts")
templates = Jinja2Templates(directory="templates")

app.mount("/assets", StaticFiles(directory="templates/assets"), name="assets")
app.mount("/category/assets", StaticFiles(directory="templates/assets"), name="assets")

sentry_sdk.init(
    "https://78b74e6eaeef42388893a8cf0a4c332e@o309026.ingest.sentry.io/5889732",
    traces_sample_rate=1.0
)


@app.get("/", response_class=HTMLResponse)
async def get_root(request: Request, search: Optional[str] = None):
    if search is not None:
        return templates.TemplateResponse("index.html", {"request": request, "tools": htmlgen.search(search)})
    return templates.TemplateResponse("index.html", {"request": request, "tools": htmlgen.tools("all")})

@app.get("/category/{tag}", response_class=HTMLResponse)
async def get_category(request: Request, tag: str):
    return templates.TemplateResponse("index.html", {"request": request, "tools": htmlgen.tools(tag)})

@app.get("/about", response_class=HTMLResponse)
async def get_about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/help", response_class=HTMLResponse)
async def get_about(request: Request):
    return templates.TemplateResponse("help.html", {"request": request})

@app.get("/add", response_class=HTMLResponse)
async def get_add(request: Request, show: Optional[str] = None):
    if show == "success":
        alert = htmlgen.alert("add-success")
    elif show == "error":
        alert = htmlgen.alert("add-error")
    else:
        alert = """"""
    return templates.TemplateResponse("add.html", {"request": request, "alert": alert, "options": htmlgen.category_options()})

@app.post("/add/submit")
async def post_add_submit(name: str = Form(...), category: str = Form(...), description: str = Form(...), image: UploadFile = File(...), link: str = Form(...), pricing: str = Form(...), email: str = Form(...)):
    try:
        r = requests.post("https://api.imgbb.com/1/upload?key={0}".format(os.getenv("IMGBB_TOKEN")), data={"image": base64.b64encode(image.file.read())})
        data = json.loads(r.content)["data"]
        tools.insert({
            "name": name,
            "img": data["url"],
            "category": category,
            "staffpick": False,
            "description": description,
            "link": link,
            "pricing": pricing,
            "email": email,
            "show": False
        })
        return RedirectResponse(url="/add?show=success", status_code=status.HTTP_303_SEE_OTHER)
    except:
        return RedirectResponse(url="/add?show=error", status_code=status.HTTP_303_SEE_OTHER)

@app.exception_handler(StarletteHTTPException)
async def my_custom_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse("error.html", {"request": request, "code": "404", "description": "The requested resource couldn't be found."})
    elif exc.status_code == 500:
        return templates.TemplateResponse("error.html", {"request": request, "title": "500", "description": exc.detail})
    else:
        return templates.TemplateResponse('error.html', {"request": request, "title": "Error", "description": exc.detail})

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=80)