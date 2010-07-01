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
import datetime

class CacheModelManager(models.Manager):
    def get_by_pk(self, pk, cache_timeout=None):
        if cache_timeout is None:
            cache_timeout = getattr(settings, 'CACHE_TIMEOUT', 900)
        key = self.model.cache_key("by_pk", pk)
        obj = cache.get(key)
        if obj is None:
            obj = self.get(pk=pk)
            cache.set(key, obj, cache_timeout)
        return obj

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
        cache.delete(self.cache_key("by_pk", self.pk))
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
        if cache_timeout is None:
            cache_timeout = getattr(settings, 'CACHE_TIMEOUT', 900)
        key = self.model.cache_key("by_slug", slug)
        obj = cache.get(key)
        if obj is None:
            obj = self.get(slug=slug)
            cache.set(key, obj, cache_timeout)
        return obj
        

class SlugModel(DefaultModel):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, unique=True)
    objects = SlugModelManager()

    class Meta:
        abstract = True
    def __unicode__(self):
        return self.name
    def flush_cache(self):
        super(SlugModel, self).flush_cache()
        cache.delete(self.cache_key("by_slug", self.slug))



def cached_method(cache_timeout, cache_key):
    def decorator(target):
        def wrapper(self, *args, **kwargs):
            if callable(cache_key):
                key = cache_key(self) 
            else:
                key = cache_key

            if not isinstance(key, (unicode, str)):
                key = '_'.join( str(a) for a in key )
            key = self.__class__.__name__ + '_' + key

            chunk = cache.get(key)
            if chunk is None:
                chunk = target(self, *args, **kwargs)
                if chunk is not None:
                    cache.set(key, chunk, cache_timeout)
            return chunk

        return wrapper
    return decorator

