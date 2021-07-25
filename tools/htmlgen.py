import jinja2
from dotenv import load_dotenv
from deta import Deta
import os

load_dotenv()
deta = Deta(os.getenv("DETA_TOKEN"))
toolsdb = deta.Base("whatdevsneed-posts")

all_categories = [
    {"name": "A/B Testing", "tag": "ab-testing", "color": "#f4b90a"},
    {"name": "Analytics", "tag": "analytics", "color": "#f4b90a"}, 
    {"name": "APIs", "tag": "apis", "color": "#f4b90a"}, 
    {"name": "Automation", "tag": "automation", "color": "#f4b90a"}, 
    {"name": "Backups", "tag": "backups", "color": "#f4b90a"}, 
    {"name": "Blockchain", "tag": "blockchain", "color": "#f4b90a"}, 
    {"name": "Blogging", "tag": "blogging", "color": "#f4b90a"}, 
    {"name": "Collaboration", "tag": "collaboration", "color": "#f4b90a"},
    {"name": "Community", "tag": "community", "color": "#f4b90a"}, 
    {"name": "Continuous Integrations", "tag": "continuous-integrations", "color": "#f4b90a"}, 
    {"name": "Databases", "tag": "databases", "color": "#f4b90a"}, 
    {"name": "Design", "tag": "design", "color": "#f4b90a"}, 
    {"name": "Domains", "tag": "domains", "color": "#f4b90a"}, 
    {"name": "Emails", "tag": "emails", "color": "#f4b90a"}, 
    {"name": "Extensions", "tag": "extensions", "color": "#f4b90a"},
    {"name": "Game Engines", "tag": "game-engines", "color": "#f4b90a"}, 
    {"name": "Hosting", "tag": "hosting", "color": "#f4b90a"}, 
    {"name": "IDEs", "tag": "ides", "color": "#f4b90a"}, 
    {"name": "Issue Tracking", "tag": "issue-tracking", "color": "#f4b90a"}, 
    {"name": "Documentation", "tag": "documentation", "color": "#f4b90a"}, 
    {"name": "Learning", "tag": "learning", "color": "#f4b90a"}, 
    {"name": "Legal", "tag": "legal", "color": "#f4b90a"}, 
    {"name": "Libraries", "tag": "libraries", "color": "#f4b90a"}, 
    {"name": "Licensing", "tag": "licensing", "color": "#f4b90a"},
    {"name": "Localization", "tag": "localization", "color": "#f4b90a"},
    {"name": "Logging", "tag": "logging", "color": "#f4b90a"},
    {"name": "Messaging", "tag": "messaging", "color": "#f4b90a"},
    {"name": "Monitoring", "tag": "monitoring", "color": "#f4b90a"},
    {"name": "Payments", "tag": "payments", "color": "#f4b90a"},
    {"name": "Performance", "tag": "performance", "color": "#f4b90a"},
    {"name": "Productivity", "tag": "productivity", "color": "#f4b90a"},
    {"name": "Publishing", "tag": "publishing", "color": "#f4b90a"},
    {"name": "Security", "tag": "security", "color": "#f4b90a"},
    {"name": "Storage", "tag": "storage", "color": "#f4b90a"}, 
    {"name": "Terminals", "tag": "terminals", "color": "#f4b90a"}, 
    {"name": "Other", "tag": "other", "color": "#f4b90a"}
]

def categorylist():
    return all_categories

def tools(tag):
    if tag == "all":
        entries = toolsdb.fetch({"show": True}).items
    else:
        name = ""
        for category in all_categories:
            if tag == category["tag"]:
                name = category["name"]
                break
        entries = toolsdb.fetch({"show": True, "category": name}).items
    
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
                "name": entry["name"],
                "category": entry["category"],
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

def categories():
    categories_html = """"""
    for category in all_categories:
        categories_html = categories_html + """<a class="btn btn-primary" role="button" style="padding-top: 0px;padding-bottom: 0px;padding-right: 5px;padding-left: 5px;background: rgba(13,110,253,0);border-radius: 10px;color: {0};margin-right: 10px;margin-bottom: 10px;border-width: 2px;border-color: {0};" href="https://whatdevsneed.com/category/{1}">{2}</a>""".format(category["color"], category["tag"], category["name"])
    return categories_html

def category_options():
    options_html = """"""
    for category in all_categories:
        options_html = options_html + """<option value="{0}">{0}</option>""".format(category["name"])
    return options_html