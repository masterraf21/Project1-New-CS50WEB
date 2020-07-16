from django.shortcuts import render
from django.urls import reverse
from markdown2 import Markdown
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
import random
from . import util

md = Markdown()


class Search(forms.Form):
    item = forms.CharField(label="Search")


class NewPage(forms.Form):
    title = forms.CharField(label="Title")
    text = forms.CharField(label="Text")


class EditPage(forms.Form):
    text = forms.CharField(label="EditedText")


def index(request):
    entries = util.list_entries()
    searched = []
    if request.method == "POST":
        form = Search(request.POST)
        if form.is_valid():
            query = form.cleaned_data["item"]
            for entry in entries:
                if query in entries:
                    entry = util.get_entry(query)
                    entry_converted = md.convert(entry)
                    return render(request, "encyclopedia/entry.html", {
                        "entry": entry_converted,
                        "title": query,
                        "form": Search()
                    })
                else:
                    if query.lower() in entry.lower():
                        searched.append(entry)
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": entries,
                "form": Search()
            })
        return render(request, "encyclopedia/search.html", {
            "searched": searched,
            "form": Search()
        })

    else:
        return render(request, "encyclopedia/index.html", {
            "entries": entries,
            "form": Search()
        })


def show_entry(request, title):
    entry = util.get_entry(title)
    entry_converted = md.convert(entry)
    if entry is None:
        return render(request, "encyclopedia/error.html")
    return render(request, "encyclopedia/entry.html", {
        "entry": entry_converted,
        "title": title,
        "form": Search()
    })


def random_page(request):
    entry_list = util.list_entries()
    rand_title = random.choice(entry_list)
    rand_entry = util.get_entry(rand_title)
    rand_entry = md.convert(rand_entry)
    return render(request, "encyclopedia/entry.html", {
        "entry": rand_entry,
        "title": rand_title,
        "form": Search()
    })


def new_page(request):
    if request.method == "POST":
        form = NewPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            entries = util.list_entries()
            if title in entries:
                return render(request, "encyclopedia/error.html", {
                    "message": "Title already exist"
                })
            else:
                util.save_entry(title, text)
                entry = util.get_entry(title)
                entry_converted = md.convert(entry)
                return render(request, "encyclopedia/entry.html", {
                    "entry": entry_converted,
                    "title": title,
                    "form": Search()
                })

        else:
            return render(request, "encyclopedia/new_page.html", {
            "form": Search(),
            "new_page": NewPage()
        })

    else:
        return render(request, "encyclopedia/new_page.html", {
            "form": Search(),
            "new_page": NewPage()
        })
