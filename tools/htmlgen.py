import jinja2
from dotenv import load_dotenv
from deta import Deta
import os

load_dotenv()
deta = Deta(os.getenv("DETA_TOKEN"))
toolsdb = deta.Base("whatdevsneed-posts")


def tools():
    entries = toolsdb.fetch({"show": True}).items
    if len(entries) == 0:
        tools_html = """<p>There's nothing here yet.</p>"""
    else:
        tools_html = """"""
        with open("templates/elements/tools.html", "r") as f:
            tools_html_template = jinja2.Template(f.read())
        for entry in entries:
            if entry["staffpick"] is True:
                staffpick_html = """<span style="font-size: 13.5px;margin-left: 10px; border-width: 2px; border-radius: 5px; border-color: #fdc80d; border-style: solid; padding: 3px; color: #c1990b;"><b>STAFF PICK</b></span>"""
            else:
                staffpick_html = """"""
            data = {
                "imgurl": entry["img"],
                "imgalt": entry["name"],
                "category": entry["category"],
                "staffpick": staffpick_html,
                "description": entry["description"],
                "link": entry["link"],
                "sharelink": "https://twitter.com/intent/tweet?url=whatdevsneed.com&text={0}".format("I just found " + entry["name"] + " on"),
                "pricing": entry["pricing"]
            }
            tools_html = tools_html + tools_html_template.render(data)
    return tools_html

def alert(id):
    if id == "add-success":
        alert = """<div role="alert" class="alert alert-success" style="margin-bottom: 80px;max-width: 80%;margin-right: auto;margin-left: auto;"><span><strong>Success!</strong> Your tool is being reviewed. You&#39;ll be notified via email when it&#39;s added.</span></div>"""
    elif id == "add-error":
        alert = """<div role="alert" class="alert alert-danger" style="margin-bottom: 80px;max-width: 80%;margin-right: auto;margin-left: auto;"><span><strong>Error!</strong> The tool couldn&#39;t be added.</span></div>"""
    return alert