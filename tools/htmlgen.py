from dotenv import load_dotenv
import jinja2
from dotenv import load_dotenv
from deta import Deta
import urllib.parse
import random
import os

load_dotenv()
deta = Deta(os.getenv("DETA_COLLECTION_KEY"))
toolsdb = deta.Base("whatdevsneed-posts")

all_categories = ["AIs", "Analytics", "APIs", "Automation", "Backups", "Blockchain", "Blogging", "Collaboration", "Community",
                  "Communication", "Continuous Integrations", "Databases", "Design", "Domains", "Emails", "Extensions", "Game Engines", "Hosting", "IDEs", 
                  "Issue Tracking", "Documentation", "Learning", "Legal", "Libraries", "Licensing", "Localization", "Logging", "Messaging", 
                  "Monitoring", "Payments", "Performance", "Productivity", "Publishing", "Security", "Software", "Storage", "Terminals", "Testing", "Other"]

free_span = """<span class="float-end" style="color: rgb(181,181,181);font-weight: 400;"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="1em" height="1em" fill="currentColor" style="font-size: 14px;margin-bottom: 3px;margin-right: 5px;color: rgb(224,189,7);">
        <!--! Font Awesome Free 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free (Icons: CC BY 4.0, Fonts: SIL OFL 1.1, Code: MIT License) Copyright 2022 Fonticons, Inc. -->
        <path d="M512 256C512 397.4 397.4 512 256 512C114.6 512 0 397.4 0 256C0 114.6 114.6 0 256 0C397.4 0 512 114.6 512 256zM256 48C141.1 48 48 141.1 48 256C48 370.9 141.1 464 256 464C370.9 464 464 370.9 464 256C464 141.1 370.9 48 256 48z"></path>
    </svg>Free (<span data-bs-toggle="tooltip" data-bs-placement="right" style="color: rgb(224,189,7);text-decoration: underline;" title="Completely free, without paid plans">?</span>)</span>"""
freemium_span = """<span class="float-end" style="color: rgb(181,181,181);font-weight: 400;"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="1em" height="1em" fill="currentColor" style="font-size: 14px;margin-bottom: 3px;margin-right: 5px;color: rgb(224,189,7);">
        <!--! Font Awesome Free 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free (Icons: CC BY 4.0, Fonts: SIL OFL 1.1, Code: MIT License) Copyright 2022 Fonticons, Inc. -->
        <path d="M512 256C512 397.4 397.4 512 256 512C114.6 512 0 397.4 0 256C0 114.6 114.6 0 256 0C397.4 0 512 114.6 512 256zM256 64V448C362 448 448 362 448 256C448 149.1 362 64 256 64z"></path>
    </svg>Freemium (<span data-bs-toggle="tooltip" data-bs-placement="right" style="color: rgb(224,189,7);text-decoration: underline;" title="Partly free, with free and paid plans">?</span>)</span>"""
paid_span = """<span class="float-end" style="color: rgb(181,181,181);font-weight: 400;"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="1em" height="1em" fill="currentColor" style="font-size: 14px;margin-bottom: 3px;margin-right: 5px;color: rgb(224,189,7);">
        <!--! Font Awesome Free 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free (Icons: CC BY 4.0, Fonts: SIL OFL 1.1, Code: MIT License) Copyright 2022 Fonticons, Inc. -->
        <path d="M512 256C512 397.4 397.4 512 256 512C114.6 512 0 397.4 0 256C0 114.6 114.6 0 256 0C397.4 0 512 114.6 512 256z"></path>
    </svg>Paid (<span data-bs-toggle="tooltip" data-bs-placement="right" style="color: rgb(224,189,7);text-decoration: underline;" title="Only paid plans available">?</span>)</span>"""

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
        with open("templates/elements/tool.html", "r") as f:
            tools_html_template = jinja2.Template(f.read())
        for entry in entries:
            if entry["staffpick"] is True:
                staffpick_html = """<span style="padding: 4px 12px;font-size: 12px;border: 2px solid rgb(224,189,7);border-radius: 8px;margin-left: 8px;">Staff-Pick</span>"""
            else:
                staffpick_html = """"""
                
            if entry["pricing"] == "Free":
                pricing_html = free_span
            elif entry["pricing"] == "Freemium":
                pricing_html = freemium_span
            elif entry["pricing"] == "Paid":
                pricing_html = paid_span
            else:
                pricing_html = f"""<span>{entry["pricing"]}</span>"""
                
            data = {
                "imgurl": entry["img"],
                "name": entry["name"],
                "category": entry["category"],
                "category_link": "/category/" + str(urllib.parse.quote(entry["category"])),
                "staffpick": staffpick_html,
                "description": entry["description"],
                "link": entry["link"]+"?ref=whatdevsneed",
                "sharelink": "https://twitter.com/intent/tweet?url=whatdevsneed.com&text={0}".format("I just found " + entry["link"] + " on"),
                "pricing": pricing_html
            }
            tools_html = tools_html + tools_html_template.render(data)
    return tools_html


def alert(id):
    if id == "add-success":
        alert = """
            <div style="margin-bottom: 32px;padding: 20px;border: 2px solid rgb(68,176,30);border-radius: 12px;color: rgb(68,176,30);">
                <p style="margin-bottom: 0px;"><span style="font-weight: 600;font-size: 18px;">Success!</span><br />Your tool was submitted for review. Check back later to see if it was added.</p>
            </div>"""
    elif id == "add-error":
        alert = """
            <div style="margin-bottom: 32px;padding: 20px;border-radius: 12px;color: rgb(200,31,72);border: 2px solid rgb(200,31,72);">
                <p style="margin-bottom: 0px;"><span style="font-weight: 600;font-size: 18px;">Error!</span><br />Your tool could not be submitted. Please try again later.</p>
            </div>"""
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