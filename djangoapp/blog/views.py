from django.shortcuts import render

# Create your views here.
def index(request):
    return render(
        request,
        'blog/pages/index.html',
        {
            # 'name': 'Ailton',
        }
    )
def page(request):
    return render(
        request,
        'blog/pages/page.html',
        {
            # 'name': 'Ailton',
        }
    )
def post(request):
    return render(
        request,
        'blog/pages/post.html',
        {
            # 'name': 'Ailton',
        }
    )