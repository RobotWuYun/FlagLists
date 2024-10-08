from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from . import models
from . import views
class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, views.home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = views.home_page(request)
        expected_html = render_to_string('home.html', request=request)
        self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_can_save_a_POST_request(self):
        inputData = 'A new list item'

        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = inputData
        response = views.home_page(request)

        self.assertEqual(models.Item.objects.count(), 1)
        new_item = models.Item.objects.first()
        self.assertEqual(new_item.text, inputData)
        

    def test_home_page_redirects_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'
        response = views.home_page(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')    
        

    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        views.home_page(request)
        self.assertEqual(models.Item.objects.count(),0)

    def test_home_page_displays_all_list_items(self):
        models.Item.objects.create(text='itemey 1')
        models.Item.objects.create(text='itemey 2')
        request = HttpRequest()
        response = views.home_page(request)
        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())

class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = models.Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = models.Item()
        second_item.text = "Item the second"
        second_item.save()

        saved_items = models.Item.objects.all()
        self.assertEqual(saved_items.count(),2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')