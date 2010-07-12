#  Copyright 2010 Concentric Sky, Inc. 
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.hashcompat import md5_constructor
from django.utils.http import urlquote


def render_template(request, *args, **kwargs):
    """Render a template using RequestContext; so ContextProcessors are used."""
    kwargs['context_instance'] = RequestContext(request)
    return render_to_response(*args, **kwargs)

def invalidate_template_cache(fragment_name, *variables):
    """Invalidate a cached template fragment created with the {%cache%} template tag."""
    args = md5_constructor(u':'.join([urlquote(var) for var in variables]))
    cache_key = 'template.cache.%s.%s' % (fragment_name, args.hexdigest())
    cache.delete(cache_key)

def paginate(request, objects, how_many=25, page_variable_name='page'):
    """Helper function to ease pagintation.

    Arguments:
      request -- request object
      objects -- the objects to paginate
      how_many -- how many objects to show per page
      page_variable_name -- the GET variable name used for page number

    """
    paginator = Paginator(objects, how_many)
    try:
        page_num = int(request.GET.get(page_variable_name,"1"))
    except ValueError:
        page_num = 1
    return paginator.page(min(paginator.num_pages, page_num))
