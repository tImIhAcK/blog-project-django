from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm
from django.views import generic
from django.core.mail import send_mail
from django.views.decorators.http import require_POST

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
    comments = post.comments.filter(active=True)
    form = CommentForm()
    
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form': form})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent=False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read "\
                f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n"\
                f"{cd['name']}\'s comment: {cd['comments']}"
            
            send_mail(subject, message, 'adeniranjohn2016@gmail.com', [cd['to']])
            sent=True
            
            
    else:
        form = EmailPostForm()
    return render(request, 'blog/post_share.html', {'form': form, 'post':post, 'sent': sent})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        
    return render(request, 'blog/post_comment.html', {'form': form, 'comment': comment, 'post': post})