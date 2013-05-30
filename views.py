#-*- coding:utf-8 -*-
"""
test
"""


from django.http import HttpResponse





def hello(request):
    print 'hello........'
    return HttpResponse('hello world')

