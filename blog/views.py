from django.shortcuts import render, get_object_or_404, reverse
# from django.http import HttpResponse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Post, Comment
from .forms import CommentForm

# Create your views here.
# def my_blog(request):
#     return HttpResponse("Hello, Blog!")


class PostList(generic.ListView):
    """
    View to display a list of published posts with pagination.
    """
    # model = Post
    # template_name = "post_list.html"
    # filter(author=2) # all().order_by("-created_on")
    queryset = Post.objects.filter(status=1)
    template_name = "blog/index.html"
    paginate_by = 6


def post_detail(request, slug):
    """
    Display an individual :model:`blog.Post`.

    **Context**

    ``post``
        An instance of :model:`blog.Post`.
    ``coder``
        Coders name.
    ``comments``
        All approved comments related to the post.
    ``coment_count``
        A count of approved comments related to the post.
    ``coment_form``
        An instance of :form:`blog.CommentForm`.
    **Template:**

    :template:`blog/post_detail.html`
    """

    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comments = post.comments.all().order_by("-created_on")
    comment_count = post.comments.filter(approved=True).count()

    if request.method == "POST":
        print("Received a POST request")
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Comment submitted and awaiting approval'
            )

    comment_form = CommentForm()  # resets content of form
    print("About to render template")

    return render(
        request,
        "blog/post_detail.html",
        {
            "post": post,
            "coder": "Andy",
            "comments": comments,
            "comment_count": comment_count,
            "comment_form": comment_form,
        },  # context
    )


def comment_edit(request, slug, comment_id):
    """
    Display an individual comment for edit.

    **context**

    ``post``
        An instance of :model:`blog.Post`.
    ``comments``
        A single comment related to the post.
    ``coment_form``
        An instance of :form:`blog.CommentForm`.
    """
    if request.method == "POST":

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id)
        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.author == request.user:
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.approved = False
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment Updated!')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Error updating comment!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))


def comment_delete(request, slug, comment_id):
    """
    Delete an individual comment.

    **context**

    ``post``
        An instance of :model:`blog.Post`.
    ``comments``
        A single comment related to the post.
    """
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
    else:
        messages.add_message(request, messages.ERROR,
                             'You can only delete your own comments!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))
