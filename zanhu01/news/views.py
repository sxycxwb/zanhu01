#!/usr/bin/python3
# _*_ coding:utf-8
# __author__ = 'summer'

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,DeleteView
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.urls import reverse,reverse_lazy

from zanhu01.news.models import News
from zanhu01.helper import ajax_required,AuthorRequireMixin


class NewsListView(LoginRequiredMixin, ListView):
    """首页动态"""
    model = News
    paginate_by = 20  # url中的? page=
    template_name = "news/news_list.html"  # 模型类名_list.html

    # queryset = News.objects.all()
    # page_kwarg = 'p' # 为url重的page参数重命名
    # context_object_name = 'news_list'  # 默认值是'模型类名_list' 或者'object_list'
    # ordering = 'created_at'  # ('x','y')

class NewsDeleteView(LoginRequiredMixin,AuthorRequireMixin,DeleteView):
    model = News
    template_name = 'news/news_confirm_delete.html'
    slug_url_kwarg = 'slug'#通过url传入要删除的对象主键id，默认值是slug
    pk_url_kwarg = 'pk'#通过url传入要删除的对象主键id,默认是pk
    success_url = reverse_lazy('news:list') #项目URLConf未加载前使用

@login_required
@ajax_required
@require_http_methods(['POST'])
def post_new(request):
    """发送动态，AJAX POST请求"""
    post = request.POST['post'].strip()
    if post:
        posted = News.objects.create(user=request.user, content=post)
        html = render_to_string('news/news_single.html', {'news': posted, 'request': request})
        return HttpResponse(html)
    else:
        return HttpResponseBadRequest('内容不能为空')
