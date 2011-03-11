from django import http
from django import template
from django.conf import settings


def error500(request, template_name='500.html'):
    t = template.loader.get_template(template_name)
    context = template.Context({
        'MEDIA_URL': settings.MEDIA_URL,
    })
    return http.HttpResponseServerError(t.render(context))

def error404(request, template_name='404.html'):
    t = template.loader.get_template(template_name)
    context = template.Context({
        'MEDIA_URL': settings.MEDIA_URL,
    })
    return http.HttpResponseNotFound(t.render(context))


def robots_txt(request):
    return http.HttpResponse("User-agent: *\nDisallow: /\n", content_type='text/plain');
