# -*- coding: utf-8 -*-
#from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators import csrf
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template import loader
from django.http import (
    Http404, HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect,
)


def index(request):  # index页面需要一开始就加载的内容写在这里
	context = {}
	# response = render_to_response('index.html', context, context_instance=RequestContext(request))
	template_name = 'index.html'

	content = loader.render_to_string(template_name, context, request)
	response = HttpResponse(content)
	# header('X-Frame-Options: allow-from http://lemon.v');
	# header("Content-Security-Policy: frame-ancestors lemon.v; frame-src lemon.v;");
	response.__setitem__("X-Frame-Options", "allow-from http://192.168.0.110:7474")
	response.__setitem__("Content-Security-Policy", "frame-ancestors http://192.168.0.110:7474; frame-src http://192.168.0.110:7474;")
	return response
	# return render(request, 'index.html', context)
	