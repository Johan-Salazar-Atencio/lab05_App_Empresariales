import copy

from django.apps import AppConfig
from django.template import context


def _fixed_context_copy(self):
    duplicate = copy.copy(super(context.BaseContext, self).__selfclass__.__new__(self.__class__))
    duplicate.dicts = self.dicts[:]
    return duplicate


def _patch_context_copy():
    if hasattr(context.BaseContext, '_py314_patched'):
        return

    def __copy__(self):
        duplicate = self.__class__.__new__(self.__class__)
        duplicate.__dict__.update(self.__dict__)
        duplicate.dicts = self.dicts[:]
        return duplicate

    context.BaseContext.__copy__ = __copy__
    context.BaseContext._py314_patched = True


class MoviesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies'
    verbose_name = 'Movies'

    def ready(self):
        _patch_context_copy()
