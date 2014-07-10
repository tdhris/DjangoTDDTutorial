from django.shortcuts import render, redirect
from lists.models import Item, List
from django.core.exceptions import ValidationError


def home_page(request):
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})


def view_list(request, list_id):
    data = {}
    list_ = List.objects.get(id=list_id)
    data['list'] = list_
    if request.method == 'POST':
        item = Item.objects.create(text=request.POST['item_text'], list=list_)
        try:
            item.save()
            return redirect(list_)
        except ValidationError:
            data['error'] = "You can't have an empty list item"
    return render(request, 'list.html', data)


def new_list(request):
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list=list_)
    try:
        item.save()
        item.full_clean()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {'error': error})
    return redirect('view_list', list_.id)
