from django.shortcuts import render
from .models import About

# Create your views here.
def about_me(request):
    """
    Renders most recently created :model:`about.About`
    in About page
    """

    about = About.objects.all().order_by("-updated_on").first()

    return render(
        request,
        "about/about.html",
        {"about": about},  # context
    )
