from django.test import TestCase
from django.urls import resolve
from .views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
import re
from .models import Item

class HomePageTest(TestCase):
    # render_to_string로 받은 html 데이터와 response.content.decode()로 받은 html 데이터가 같지 않다.
    # render_to_string에 request=request를 해도 값이 같아지지 않아 csrf의 값을 삭제한다
    def remove_csrf(self, origin):
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        return re.sub(csrf_regex, '', origin)

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = self.remove_csrf(render_to_string('home.html', request=request))
        self.assertEqual(self.remove_csrf(response.content.decode()), expected_html)

        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>To-Do lists</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))

    def test_home_page_can_save_a_POST_request(self):
        # 설정(SetUp)
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = '신규 작업 아이템'

        # 처리(Exercise)
        response = home_page(request)

        #어설션(Assert)
        self.assertIn('신규 작업 아이템', response.content.decode())
        expected_html = self.remove_csrf(render_to_string(
            'home.html',
            {'new_item_text': '신규 작업 아이템'},
            request=request,
        ))
        self.assertEqual(self.remove_csrf(response.content.decode()), expected_html)

class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = '첫 번째 아이템'
        first_item.save()

        second_item = Item()
        second_item.text = '두 번째 아이템'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, '첫 번째 아이템')
        self.assertEqual(second_saved_item.text, '두 번째 아이템')