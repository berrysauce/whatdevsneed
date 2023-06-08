import os
import uuid
import boto3
import random
import urllib
import uvicorn
import requests
from deta import Deta
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()

app = FastAPI(
    docs_url=None, 
    redoc_url=None, 
    title="whatdevsneed API", 
    description="API for whatdevsneed.com"
)
deta = Deta(os.getenv("DETA_COLLECTION_KEY"))
db = deta.Base("whatdevsneed-posts")

# add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

def get_s3_client():
    session = boto3.session.Session()
    client = session.client(
        "s3",
        region_name="nl-ams",
        endpoint_url="https://s3.nl-ams.scw.cloud",
        aws_access_key_id=os.getenv("S3_ACCESS_TOKEN"),
        aws_secret_access_key=os.getenv("S3_SECRET_TOKEN")
    )
    return client


def filter_item(item):
    item_data = {
        "key": item["key"],
        "image_url": item["img"],
        "name": item["name"],
        "description": item["description"],
        "category": item["category"],
        "tool_url": item["link"],
        "share_url": "https://twitter.com/intent/tweet?url=whatdevsneed.com&text={0}".format("I just found " + item["link"] + " on"),
        "pricing": item["pricing"],
        "staff_pick": item["staffpick"]
    }
    return item_data


@app.get("/", response_class=HTMLResponse)
async def get_root():
    return f"This is the API for whatdevsneed.com – Source code available at https://github.com/berrysauce/whatdevsneed – Copyright {datetime.now().year} berrysauce"
    

@app.get("/get/tools/{category}")
async def get_tools(category: str):
    if category == "all":
        db_items = db.fetch({"show": True}).items   
    else:
        db_items = db.fetch({"show": True, "category": urllib.parse.unquote(category)}).items
    
    tools = []
    for item in db_items:
        tools.append(filter_item(item))
        
    # shuffle for good fun & return
    random.shuffle(tools)
    return tools


@app.get("/get/search")
async def get_search(q: str):
    tools = []
    for item in db.fetch({"show": True}).items:
        if q.lower() in str(item["name"]).lower() or q.lower() in str(item["description"]).lower() or q.lower() in str(item["category"]).lower():
            tools.append(filter_item(item))
            
    # shuffle for good fun & return
    random.shuffle(tools)
    return tools


@app.post("/post/submit")
async def post_submit(
    name: str = Form(...),
    category: str = Form(...),
    description: str = Form(...),
    image: UploadFile = File(...),
    link: str = Form(...),
    pricing: str = Form(...)
):
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
        ACL="public-read",
        Bucket="cdn.whatdevsneed.com",
        Key=f"img/{img_name}"
    )

    # Add to database
    db.insert({
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
    requests.post(f"https://push.techulus.com/api/v1/notify/{api_key}?title={title}&body={body}")

    return {"detail": "Submission successful"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)