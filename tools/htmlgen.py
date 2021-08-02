from dotenv.main import rewrite
import jinja2
from dotenv import load_dotenv
from deta import Deta
import os
import urllib.parse
import random

load_dotenv()
deta = Deta(os.getenv("DETA_TOKEN"))
toolsdb = deta.Base("whatdevsneed-posts")

all_categories = ["A/B Testing", "AIs", "Analytics", "APIs", "Automation", "Backups", "Blockchain", "Blogging", "Collaboration", "Community",
                  "Communication", "Continuous Integrations", "Databases", "Design", "Domains", "Emails", "Extensions", "Game Engines", "Hosting", "IDEs", 
                  "Issue Tracking", "Documentation", "Learning", "Legal", "Libraries", "Licensing", "Localization", "Logging", "Messaging", 
                  "Monitoring", "Payments", "Performance", "Productivity", "Publishing", "Security", "Software", "Storage", "Terminals", "Other"]

def categorylist():
    return all_categories

def search(query):
    search = toolsdb.fetch({"show": True}).items
    entries = []
    for entry in search:
        if query.lower() in str(entry["name"]).lower() or query.lower() in str(entry["description"]).lower() or query.lower() in str(entry["category"]).lower():
            entries.append(entry)
    return tools_html(entries)

def tools(tag):
    if tag == "all":
        entries = toolsdb.fetch({"show": True}).items   
    else:
        entries = toolsdb.fetch({"show": True, "category": urllib.parse.unquote(tag)}).items
    return tools_html(entries)

def tools_html(entries):
    if len(entries) == 0:
        tools_html = """<p>There's nothing here yet.</p>"""
    else:
        random.shuffle(entries)
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
                "name": entry["name"],
                "category": entry["category"],
                "category_link": "/category/" + str(urllib.parse.quote(entry["category"])),
                "staffpick": staffpick_html,
                "description": entry["description"],
                "link": entry["link"],
                "sharelink": "https://twitter.com/intent/tweet?url=whatdevsneed.com&text={0}".format("I just found " + entry["link"] + " on"),
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

#def categories():
#    categories_html = """"""
#    for category in all_categories:
#        categories_html = categories_html + """<a class="btn btn-primary" role="button" style="padding-top: 0px;padding-bottom: 0px;padding-right: 5px;padding-left: 5px;background: rgba(13,110,253,0);border-radius: 10px;color: {0};margin-right: 10px;margin-bottom: 10px;border-width: 2px;border-color: {0};" href="https://whatdevsneed.com/category/{1}">{2}</a>""".format(category["color"], category["tag"], category["name"])
#    return categories_html

def category_options():
    options_html = """"""
    for category in all_categories:
        options_html = options_html + """<option value="{0}">{0}</option>""".format(category)
    return options_html