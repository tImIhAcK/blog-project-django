from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views import generic

# Create your views here.
class PostListView(generic.ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post_list.html'

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                            status=Post.Status.PUBLISHED,
                            slug=post,
                            publish__year=year,
                            publish__month=month,
                            publish__day=day)
    
    return render(request, 'blog/post_detail.html', {'post': post})
