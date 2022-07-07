from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from markdown2 import markdown
from django import forms
from random import choice
from . import util


class EditTextForm(forms.Form):
    title =  forms.CharField(label = '', widget=forms.TextInput(attrs={'readonly':'readonly', 'class':'form-control'}))
    body = forms.CharField(label = '', widget=forms.Textarea(attrs={'rows':'15', 'class':'form-control'}))

class NewTextForm(forms.Form):
    title =  forms.CharField(label = '', widget=forms.TextInput(attrs={'placeholder':'Введіть назву статті', 'class':'form-control'}))
    body = forms.CharField(label = '', widget=forms.Textarea(attrs={'placeholder':'Створіть текст статті та натисніть кнопку < Зберегти >', 'rows':'15', 'class':'form-control'}))

def index(request):
    page_header = "Всі сторінки Wiki"
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "header": page_header
    })


def search(request):
    q = request.GET.get("q")
    entry_text = util.get_entry(q)
    if entry_text == None:
        entries = util.list_entries()
        search_entries = []
        for i in entries:
            if i.lower().find(q.lower()) != -1:
                search_entries.append(i)
        if len(search_entries) == 0:
            page_header = "Нічого не знайдено"
        else:
            page_header = "Результати пошуку"
        return render(request, "encyclopedia/index.html", {
            "entries": search_entries,
            "header": page_header
            })
    else:
        return render(request, "wiki/page.html", {
            "entry_text": markdown(entry_text),
            "entry_name": q,
            "edit": True
            })


def page(request, entry):
    entry_text = util.get_entry(entry)
    if entry_text == None:
       entry_text = f"Сторінка {entry} не знайдена." 
    else:
       entry_text = markdown(entry_text)
    return render(request, "wiki/page.html", {
        "entry_text": entry_text,
        "entry_name": entry
    })


def edit(request):
     if request.method == "POST":
        title = request.POST.get('title')
        form = EditTextForm()
        form.fields['title'].initial = title
        form.fields['body'].initial = util.get_entry(title)
        return render(request, "wiki/editpage.html", {
            "form": form,
            "edit": True 
        })


def save(request):
    if request.method == "POST":
        form = EditTextForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            body = form.cleaned_data['body'].encode('utf-8')
            edit = request.POST.get('edit')
            if edit == "True":
                util.save_entry(title, body)
        return render(request, "wiki/page.html", {
            "entry_text": markdown(body),
            "entry_name": title, 
            })


def new(request):
    if request.method == "POST":
        form = NewTextForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            edit = request.POST.get('edit')
            if edit != "True":
                entries = util.list_entries()
                for entry in entries:
                    if entry.lower() == title.lower():
                        return render(request, "wiki/page.html", {
                        "entry_text": f"Сторінка {entry} вже існує.",
                        "entry_name": entry
                        })
            util.save_entry(title, body)
            return render(request, "wiki/page.html", {
                "entry_text": markdown(body),
                "entry_name": title
                })
    return render(request, "wiki/newpage.html", {
        "form": NewTextForm()
    })



def random_page(request):
    entries = util.list_entries()
    entry = choice(entries)
    return redirect(f"wiki/{entry}/")


