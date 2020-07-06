from django.shortcuts import render
from django.http import JsonResponse
from .models import Post

def posts(request):
    response = []
    posts = Post.objects.filter().order_by('-datatime')
    for post in posts:
        response.append(
            {
                'datatime': post.datatime,
                'content': post.content,
                'author': f"{post.user.first_name} {post.user.last_name}",
                'hash_content': post.hash,
                'hash_trans': post.txId
            }
        )
    return JsonResponse(response, safe=False)
# Create your views here.
