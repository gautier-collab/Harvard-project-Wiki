import markdown2, re, random
from . import util
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def entry(request, title):
    try:
        content=util.get_entry(title)
        return render(request,"encyclopedia/entry.html",{
                "title": title,
                "content":markdown2.markdown(content)
            })
    except:
        return render(request, "encyclopedia/error.html")

def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html")
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if util.get_entry(title):
            return render(request, "encyclopedia/create.html",{
                "title": title,
                "content": content,
                "already_existing": True
            })
        else:
            re1 =  re.compile(r"[ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789ÀàÁáÂâÃãÄäÇçÈèÉéÊêËëÌìÍÎîÏïÑñÒòÓóÔôÕõÖöŠšÚùÛúÜûÙüÝýŸÿŽ\-\._~:#@!&'\(\)\*\+,;= ]*$");
            if re1.match(title):
                # All chars are valid
                util.save_entry(title, content)
                return HttpResponseRedirect(f"/wiki/{title}")
            else:
                # Not all chars are valid
                return render(request, "encyclopedia/create.html",{
                    "title": title,
                    "content": content,
                    "invalid_character": True
                })

def edit(request, title):
    if request.method == "GET":
        content=util.get_entry(title)
        return render(request,"encyclopedia/edit.html",{
            "title": title,
            "content":content
        })
    if request.method == "POST":
        title = title
        content = request.POST.get("content")
        util.save_entry(title, content)
        return HttpResponseRedirect(f"/wiki/{title}")

def redirect(request):
    if request.method == "POST":
        keywords = request.POST.get("keywords")
        try:
            content=util.get_entry(keywords)
            return render(request,"encyclopedia/entry.html",{
                    "title": keywords,
                    "content":markdown2.markdown(content)
                })
        except:
            results = []
            for entry in util.list_entries():
                if keywords.lower() in entry.lower():
                    results.append(entry)
            return render(request, "encyclopedia/results.html", {
                "keywords": keywords,
                "results": results
            })

def randomPage(request):
    entryQtity = len(util.list_entries())
    index = random.randint(0,entryQtity-1)
    title = util.list_entries()[index]
    return HttpResponseRedirect(f"/wiki/{title}")