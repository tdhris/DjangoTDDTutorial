
from lists.models import Item, List
from django.test import TestCase


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='The first (ever) list item', list=list_)
        Item.objects.create(text='Item the second', list=list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')


class ListAndItemModelsTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'itemey 1')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'itemey 2')
        self.assertEqual(second_saved_item.list, list_)
