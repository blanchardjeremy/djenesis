import datetime

def default_context(request):
    """Context that will be present in EVERY RequestContext."""
    context = {
        'referer': request.META.get('HTTP_REFERER'),
        'now': datetime.datetime.now(),
    }
    return context
