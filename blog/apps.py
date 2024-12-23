from django.apps import AppConfig


class BlogConfig(AppConfig):
    """
    App configuration for the 'blog' application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
