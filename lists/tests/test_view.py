from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from lists.models import Item,List
from django.utils.html import escape
from lists.forms import ItemForm,ExistingListItemForm,DUPLICATE_ITEM_ERROR,EMPTY_ITEM_ERROR
from unittest import skip

#from django.template.loader import  render_to_string

# Create your tests here.
class HomePageTest (TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found=resolve('/')
        self.assertEqual(found.func,home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
        self.assertIsInstance(response.context['form'],ItemForm)

class ListViewTest(TestCase):
    def test_users_list_template(self):
        list_=List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_passes_correct_list_to_template(self):
        List.objects.create()
        list_=List.objects.create()
        response=self.client.get(f'/lists/{list_.id}/')
        self.assertEqual(response.context['list'],list_)

    def test_displays_all_list_items(self):
        list_=List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)
        other_list_=List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list_)
        Item.objects.create(text='other list item 2', list=other_list_)
        response=self.client.get(f'/lists/{list_.id}/')
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, "other list item 1")
        self.assertNotContains(response, "other list item 2")

    def test_can_save_a_POST_request_to_an_existing_list(self):
        List.objects.create()
        correct_list=List.objects.create()

        response=self.client.post(f'/lists/{correct_list.id}/',data={'text':'A new item for an existing list'})
        self.assertEqual(Item.objects.count(),1)
        new_item=Item.objects.first()
        self.assertEqual(new_item.text,'A new item for an existing list')
        self.assertEqual(new_item.list,correct_list)

    def test_redirects_to_list_view(self):
        List.objects.create()
        correct_list=List.objects.create()

        response = self.client.post(
            f"/lists/{correct_list.id}/",
            data={'text':'A new item for an existing list'}
        )

        self.assertRedirects(response,f'/lists/{correct_list.id}/')

    def test_validation_errors_end_up_lists_page(self):
        list_=List.objects.create()
        response=self.client.post(
            f'/lists/{list_.id}/',
            data={'text':''}
        )
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'list.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response,expected_error)

    def test_displays_item_from(self):
        list_=List.objects.create()
        response=self.client.get(f'/lists/{list_.id}/')
        self.assertIsInstance(response.context['form'],ExistingListItemForm)
        self.assertContains(response,'name="text"')

class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new',data={'text':'A new list item'})
        self.assertEqual(Item.objects.count(),1)
        new_item=Item.objects.first()
        self.assertEqual(new_item.text,'A new list item')

    def test_redirects_after_POST(self):
        response=self.client.post('/lists/new',data={'text':'A new list item'})

        new_list=List.objects.first()
        self.assertRedirects(response,f'/lists/{new_list.id}/')
        response2=self.client.get(response['location'])
        self.assertEqual(response2.status_code,200)

    def test_for_invalid_input_renders_home_template(self):
        response=self.client.post('/lists/new',data={'text':''})
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'home.html')

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post('/lists/new', data={'text': ''})
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertIsInstance(response.context['form'],ItemForm)

    def test_validation_errors_not_write_to_db(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(),0)
        self.assertEqual(List.objects.count(),0)

    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_,text="textey")
        response = self.client.post(f'/lists/{list_.id}/', data={'text': "textey"})
        expected_error=escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response,'list.html')
        self.assertEqual(Item.objects.all().count(),1)



