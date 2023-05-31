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
import boto3
import uuid


load_dotenv()

app = FastAPI()
deta = Deta(os.getenv("DETA_COLLECTION_KEY"))
tools = deta.Base("whatdevsneed-posts")
templates = Jinja2Templates(directory="templates")

app.mount("/assets", StaticFiles(directory="templates/assets"), name="assets")
app.mount("/category/assets", StaticFiles(directory="templates/assets"), name="assets")

def get_s3_client():
    session = boto3.session.Session()
    client = session.client(
        's3',
        region_name='nl-ams',
        endpoint_url='https://s3.nl-ams.scw.cloud',
        aws_access_key_id=os.getenv("S3_ACCESS_TOKEN"),
        aws_secret_access_key=os.getenv("S3_SECRET_TOKEN")
    )
    return client


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
async def post_add_submit(name: str = Form(...), category: str = Form(...), description: str = Form(...), image: UploadFile = File(...), link: str = Form(...), pricing: str = Form(...)):
    try:
        # Upload image
        img_name = str(uuid.uuid4()) + "." + image.filename.rsplit(".", 1)[1]
        img_content = image.file.read()

        # Get S3 client
        client = get_s3_client()
        # Upload
        client.put_object(
            Body=img_content,
            Bucket="cdn.whatdevsneed.com",
            Key=f"img/{img_name}",
            ContentType=image.content_type
        )
        # Set public
        client.put_object_acl(
            ACL='public-read',
            Bucket="cdn.whatdevsneed.com",
            Key=f"img/{img_name}"
        )

        # Add to database
        tools.insert({
            "name": name,
            "img": f"https://cdn.whatdevsneed.com/img/{img_name}",
            "category": category,
            "staffpick": False,
            "description": description,
            "link": link,
            "pricing": pricing,
            "show": False
        })

        # Send push
        api_key = os.getenv("PUSH_TOKEN")
        title = "[wdn] New submission"
        body = f"{name} ({category})"
        push_res = requests.post(f"https://push.techulus.com/api/v1/notify/{api_key}?title={title}&body={body}")

        return RedirectResponse(url="/add?show=success", status_code=status.HTTP_303_SEE_OTHER)
    except:
        return RedirectResponse(url="/add?show=error", status_code=status.HTTP_303_SEE_OTHER)

@app.exception_handler(StarletteHTTPException)
async def my_custom_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse("error.html", {"request": request, "code": "404", "detail": "The requested resource couldn't be found."})
    elif exc.status_code == 500:
        return templates.TemplateResponse("error.html", {"request": request, "code": "500", "detail": exc.detail})
    else:
        return templates.TemplateResponse('error.html', {"request": request, "code": "Error", "detail": exc.detail})

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)