from django.core.cache import cache
import random
import string

def ns_key(namespace, key):
  if not isinstance(namespace, (unicode, str)):
    namespace = '_'.join(str(a) for a in namespace)
  key_prefix = cache.get("__namespace_%s" % (namespace,))
  if key_prefix is None:
    key_prefix = ''.join( random.choice(string.letters) for i in range(1,8) )
    cache.set("__namespace_%s" % (namespace,), key_prefix, 900)
  return '%s_%s_%s' % (key_prefix, namespace, key)

def ns_flush(namespace):
  if not isinstance(namespace, (unicode, str)):
    namespace = '_'.join(str(a) for a in namespace)
  cache.delete("__namespace_%s" % (namespace,))
