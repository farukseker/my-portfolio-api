from django.test import TestCase
from django.shortcuts import reverse, resolve_url
from contents.models import ContentModel, ContentTypeModel


class CommentCreateTest(TestCase):

    def __init__(self, *args, **kwargs):
        self.content_type_name = 'test'
        self.create_comment_path = 'api:project:comment'
        self.valid_comment = {
            'name': 'test',
            'email': 'test@test.com',
            'comment': 'comment'
        }

        self.un_valid_comment = {
            'name': 'test',
            'email': 'test',
            'comment': 'comment'
        }

        self.empty_comment = {
            'name': '',
            'email': 'test@test.com',
            'comment': ''
        }
        super().__init__(*args, **kwargs)

    def setUp(self):
        self.content_type = self.create_contenttype()
        self.available_content = self.create_test_content(available=True)
        self.unavailable_content = self.create_test_content(available=False)

    def get_content_path(self, slug: str):
        return reverse(self.create_comment_path, kwargs={"slug":slug})

    def create_contenttype(self):
        content_type, created = ContentTypeModel.objects.get_or_create(name=self.content_type_name)
        return content_type

    def create_test_content(self, available: bool):
        return ContentModel.objects.create(**{
            'title': 'text',
            'show': available,
            'seo_description': 'seo_description',
            'content_type': self.content_type
        })

    def test_valid_comment(self):
        # Existing content must be interpreted correctly
        response = self.client.post(
            self.get_content_path(self.available_content.slug),
            data=self.valid_comment
        )
        self.assertEqual(response.status_code, 201)

    def test_valid_comment_hidden_content(self):
        # It is not possible to comment correctly on existing but hidden content.
        response = self.client.post(
            self.get_content_path(self.unavailable_content.slug),
            data=self.valid_comment
        )
        self.assertEqual(response.status_code, 404)

    def test_un_valid_comment(self):
        # The correct e-mail address must be entered in the current content.
        response = self.client.post(
            self.get_content_path(self.available_content.slug),
            data=self.un_valid_comment
        )
        self.assertEqual(response.status_code, 406)

    def test_empty_comment(self):
        # Empty comments and names cannot be sent to existing content.
        response = self.client.post(
            self.get_content_path(self.available_content.slug),
            data=self.empty_comment
        )
        self.assertEqual(response.status_code, 406)

    def test_valid_comment_non_content(self):
        # You cannot comment on content that does not exist
        response = self.client.post(
            self.get_content_path('non-content-slug'),
            data=self.empty_comment
        )
        self.assertEqual(response.status_code, 404)
