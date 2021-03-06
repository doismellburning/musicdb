import re
import itertools

from django.db import models

from musicdb.utils import slugify

class DenormalisedCharField(models.CharField):
    def __init__(self, attr, *args, **kwargs):
        # Set a longer max_length by default
        kwargs['max_length'] = kwargs.pop('max_length', 100)
        kwargs['db_index'] = kwargs.pop('db_index', True)
        kwargs['editable'] = kwargs.pop('editable', False)

        super(DenormalisedCharField, self).__init__(*args, **kwargs)

        self.attr = attr

    def pre_save(self, obj, add):
        val = getattr(obj, self.attr)

        if callable(val):
            val = val()

        return val[:self.max_length]

    def deconstruct(self):
        name, _, _, kwargs = super(DenormalisedCharField, self).deconstruct()

        return (
            name,
            'musicdb.db.fields.DenormalisedCharField',
            (self.attr,),
            kwargs,
        )

class MySlugField(DenormalisedCharField):
    def __init__(self, *args, **kwargs):
        self.filter = kwargs.pop('filter', None)

        super(MySlugField, self).__init__(*args, **kwargs)

    def pre_save(self, obj, add):
        val = super(MySlugField, self).pre_save(obj, add)
        val = slugify(val)[:self.max_length]

        val_to_prepend = val[:self.max_length - 3]

        qs = obj.__class__.objects.all()

        if self.filter is not None:
            qs = getattr(obj, self.filter)()

        for count in itertools.count(1):
            filters = {
                self.name: val,
            }

            if not qs.filter(**filters).exclude(pk=obj.pk).exists():
                return val

            val = '%s-%d' % (val_to_prepend, count)

class FirstLetterField(DenormalisedCharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 1

        super(FirstLetterField, self).__init__(*args, **kwargs)

    def pre_save(self, obj, add):
        val = super(FirstLetterField, self).pre_save(obj, add).lower()

        if re.match(r'[a-z]', val):
            return val

        if re.match(r'\d', val):
            return '0'

        return '-'
