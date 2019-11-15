from django.test import TestCase, RequestFactory

from . import views
from .models import Task


class ParseUrlAjaxTests(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

    def create_post_response(self, url):
        request = self.factory.post('', {'url': url})
        return views.ParseURLAjax.as_view()(request)

    def test_get_method_returns_template(self):
        """ParseURLAjax works with get request"""
        request = self.factory.get('')
        response = views.ParseURLAjax.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_post_method_successfull_url(self):
        """post method returns successfully"""
        response = self.create_post_response('https://daomaker.com')

        self.assertEqual(response.status_code, 201)

        # object is created
        record_count = Task.objects.all().count()
        self.assertEqual(record_count, 1)

        # success message
        self.assertEqual(response.content, b'success')

    def test_post_method_schema_missing_from_url(self):
        """Test that schema is missing from url"""
        response = self.create_post_response('daomaker.com')

        self.assertEqual(response.content, b'Missing Schema(http or https)')

    def test_invalid_url(self):
        """Test that url is invalid"""
        response = self.create_post_response('http://daomaker')

        self.assertEqual(response.content, b'Please enter a valid url')

    def test_failed_url(self):
        """Test that url fails to extract all metadata"""
        response = self.create_post_response('http://facebook.com')

        self.assertEqual(response.content, b'failed')


class GetDataTests(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

        Task.objects.create(
            parsed_url='https://daomaker.com/',
            title='Daomaker1',
            description='Social Mining is the most advanced resources for'
                        ' converting any Tokenized Ecosystem into a '
                        'Decentralized Autonomous Organization (DAO)',
            site_name='Daomaker - The Creators of Social Mining',
            image_url='https://daomaker.com/wp-content/uploads/2019/08/facebook-cover-daomaker.jpg',
        )
        Task.objects.create(
            parsed_url='https://daomaker.com/',
            title='Daomaker2',
            description='Social Mining is the most advanced resources for'
                        ' converting any Tokenized Ecosystem into a '
                        'Decentralized Autonomous Organization (DAO)',
            site_name='Daomaker - The Creators of Social Mining',
            image_url='https://daomaker.com/wp-content/uploads/2019/08/facebook-cover-daomaker.jpg',
        )
        Task.objects.create(
            parsed_url='https://daomaker.com/',
            title='Daomaker3',
            description='Social Mining is the most advanced resources for'
                        ' converting any Tokenized Ecosystem into a '
                        'Decentralized Autonomous Organization (DAO)',
            site_name='Daomaker - The Creators of Social Mining',
            image_url='https://daomaker.com/wp-content/uploads/2019/08/facebook-cover-daomaker.jpg',
        )

    def test_context_data(self):
        """Test that context data exists"""
        request = self.factory.get('/show-data')
        response = views.GetData.as_view()(request)
        record_count = response.context_data['tasks'].count()

        self.assertEqual(response.status_code, 200)

        self.assertEqual(record_count, 3)

    def test_tasks_ordered_correctly(self):
        """Test that tasks are ordered by date from most recent to oldest"""

        request = self.factory.get('/show-data')
        response = views.GetData.as_view()(request)

        self.assertQuerysetEqual(
            response.context_data['tasks'],
            ['<Task: Daomaker3>', '<Task: Daomaker2>', '<Task: Daomaker1>']
        )
