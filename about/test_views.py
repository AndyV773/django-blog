from django.test import TestCase
from django.urls import reverse
from .forms import CollaborateForm
from .models import About

# Create your tests here.
class TestAboutViews(TestCase):
    """
    Testing about_me view function

    Checking collaborate_form is instance
    of CollaborateForm
    """
    def setUp(self):
        """Creates about me content"""
        self.about_content = About(title="About title",
            content="About content")
        self.about_content.save()
    
    def test_render_about_page_with_collaborate_form(self):
        """Verifies get request for about me containing a collaboration form"""
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"About title", response.content)
        self.assertIn(b"About content", response.content)
        self.assertIsInstance(
            response.context['collaborate_form'], CollaborateForm)
