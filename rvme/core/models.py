from django.contrib.auth.models import User
from model_utils.models import TimeStampedModel


class TimeStampedFieldsModel(TimeStampedModel):
    """
    Mixin that adds date_added and date_updated to a Model.
    """

    class Meta:
        abstract = True

    def fields(self, fieldlist=None):
        if fieldlist:
            fieldlist = [self._meta.get_field(f) for f in fieldlist]
        else:
            fieldlist = (self._meta.fields + self._meta.many_to_many)
        fields = []
        for f in fieldlist:
            get_choice = 'get_%s_display' % f.name
            if hasattr(self, get_choice):
                value = getattr(self, get_choice)()
            elif isinstance(f, models.ManyToManyField):
                value_list = []
                for v in getattr(self, f.name).all():
                    value_list.append(str(v))
                value = ', '.join(value_list)
            else:
                try:
                    value = getattr(self, f.name)
                except User.DoesNotExist:
                    value = None

            if f.editable and value and f.name not in ('id', 'user_ptr'):
                fields.append(
                    {
                        'label': f.verbose_name,
                        'name': f.name,
                        'value': value,
                    }
                )
        return fields
