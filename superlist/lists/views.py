from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext, loader
from lists.models import Item, List
from lists.forms import ExistingListItemForm, ItemForm
from django.http import HttpResponse
# from django.views import generic


HOME_TEMPLATE = 'home.html'
LIST_TEMPLATE = 'list.html'


def home_page(request):
    template = loader.get_template(HOME_TEMPLATE)
    context = RequestContext(request, {'form': ItemForm()})
    return HttpResponse(template.render(context))


def view_list(request, list_id):
    list_ = get_object_or_404(List, pk=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, "form": form})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        Item.objects.create(text=request.POST['text'], list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {"form": form})
