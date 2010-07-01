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

from django.conf import settings
from django.core.cache import cache
from django.db import models
from cachemodel import ns_cache
import datetime

class CacheModelManager(models.Manager):
    def get_by(self, field_name, field_value, cache_timeout=None):
        if cache_timeout is None:
            cache_timeout = getattr(settings, 'CACHE_TIMEOUT', 900)

        # cache the field names that have been used so flush_cache can purge them
        cached_field_names = cache.get( self.model.cache_key("__cached_field_names__") )
        if cached_field_names is None:
            cached_field_names = set()
        cached_field_names.add(field_name)
        cache.set(self.model.cache_key("__cached_field_names__"), cached_field_names, cache_timeout)
        
        key = self.model.cache_key("by_"+field_name, field_value)
        obj = cache.get(key)
        if obj is None:
            obj = self.get(**{field_name: field_value})
            cache.set(key, obj, cache_timeout)
        return obj

    def get_by_pk(self, pk, cache_timeout=None):
        return self.get_by("pk",pk)


class CacheModel(models.Model):
    objects = CacheModelManager()
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.flush_cache()
        super(CacheModel, self).save(*args, **kwargs)
    def delete(self, *args, **kwargs):
        self.flush_cache()
        super(CacheModel, self).delete(*args, **kwargs)
    def flush_cache(self):
        cached_field_names = cache.get( self.cache_key("__cached_field_names__") ) 
        if cached_field_names is not None:
            for field_name in cached_field_names:
                cache.delete( self.cache_key("by_"+field_name, getattr(self, field_name)) )
        self.ns_flush_cache()
    def ns_cache_key(self, *args):
        return ns_cache.ns_key(self.cache_key(self.pk), '_'.join(str(a) for a in args))
    def ns_flush_cache(self):
        ns_cache.ns_flush(self.cache_key(self.pk))

    @classmethod
    def cache_key(cls, *args):
        key = cls.__name__
        for arg in args:
            key += '_'+str(arg)
        return key


class ActiveManager(CacheModelManager):
    use_for_related_fields = True
    def get_query_set(self):
        return super(ActiveManager, self).get_query_set().filter(is_active=True)

class DefaultModel(CacheModel):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=datetime.datetime.now, editable=False)
    updated_at = models.DateTimeField(default=datetime.datetime.now, editable=False)
    objects = CacheModelManager()
    active_objects = ActiveManager()

    class Meta:
        abstract = True

class UserModel(models.Model):
    created_by = models.ForeignKey("auth.User", related_name='%(class)s_created', editable=False, default=1)
    updated_by = models.ForeignKey("auth.User", related_name='%(class)s_updated', editable=False, default=1)

    class Meta:
        abstract = True

class DefaultUserModel(UserModel, DefaultModel):
    class Meta:
        abstract = True

class SlugModelManager(CacheModelManager):
    def get_by_slug(self, slug, cache_timeout=None):
        return self.get_by("slug", slug, cache_timeout)
        

class SlugModel(DefaultModel):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, unique=True)
    objects = SlugModelManager()

    class Meta:
        abstract = True
    def __unicode__(self):
        return self.name



def cached_method(cache_timeout, cache_key):
    def decorator(target):
        def wrapper(self, *args, **kwargs):
            key = self.ns_cache_key(cache_key)
            chunk = cache.get(key)
            if chunk is None:
                chunk = target(self, *args, **kwargs)
                cache.set(key, chunk, cache_timeout)
            return chunk
        return wrapper
    return decorator

