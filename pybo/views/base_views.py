from django.shortcuts import render, get_object_or_404, redirect 
from django.core.paginator import Paginator
from django.db.models import Q

from ..models import Question

import logging
logger = logging.getLogger('pybo')


def index(request):
    logger.info("INFO 레벨로 출력")
    question_list = Question.objects.order_by('-create_date')
    kw = request.GET.get('kw','')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(answer__content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw) 
        ).distinct()
    paginator = Paginator(question_list, 10)
    page = request.GET.get('page','1')
    page_obj = paginator.get_page(page)
    context = {'question_list':page_obj, 'page':page, 'kw':kw}
    return render(request, 'pybo/question_list.html', context)
    
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question':question}
    return render(request, 'pybo/question_detail.html', context)
