from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from .forms import CommentForm
from .models import Post

# Create your tests here.
class TestBlogViews(TestCase):
    """
    Creates a user and a post instance

    Testing post_detail view function

    Checking comment_form is instance
    of CommentForm
    """
    def setUp(self):
        """Creates superuser"""
        self.user = User.objects.create_superuser(
            username="myUsername",
            password="myPassword",
            email="test@test.com"
        )
        """Creates post content"""
        self.post = Post(title="Blog title", author=self.user,
                         slug="blog-title", excerpt="Blog excerpt",
                         content="Blog content", status=1)
        self.post.save()

    def test_render_post_detail_page_with_comment_form(self):
        """Verifies get request for post detail containing a comment form"""
        response = self.client.get(reverse(
            'post_detail', args=['blog-title']))
        # print(response.content)
        # print(response.context)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Blog title", response.content)
        self.assertIn(b"Blog content", response.content)
        self.assertIn(b"Andy", response.content)
        self.assertIsInstance(
            response.context['comment_form'], CommentForm)