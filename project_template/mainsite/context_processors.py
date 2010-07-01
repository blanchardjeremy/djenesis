import datetime

def default_context(request):
  context = {
    'referer': request.META.get('HTTP_REFERER'),
    'now': datetime.datetime.now,
  }
  return context
