from django.db.models.fields.related import ForeignKey
from django.db.models.loading import get_model
import form_fields
try:
    from south.modelsinspector import add_introspection_rules
    has_south = True
except:
    has_south = False


class ChainedForeignKey(ForeignKey):
    """
    chains the choices of a previous combo box with this one
    """
    def __init__(self, to, middle=None, chained_field=None, chained_model_field=None, show_all=False, auto_choose=False, **kwargs):
        if isinstance(to, basestring):
            self.app_name, self.model_name = to.split('.')
        else:
            self.app_name = to._meta.app_label
            self.model_name = to._meta.object_name

        if middle is not None:
            if isinstance(middle, basestring):
                self.mapp_name, self.middle_name = middle.split('.')
            else:
                self.mapp_name = middle._meta.app_label
                self.middle_name = middle._meta.object_name
        else:
            self.middle_name = None
            self.mapp_name = None

        self.chain_field = chained_field
        self.model_field = chained_model_field
        self.show_all = show_all
        self.auto_choose = auto_choose

        ForeignKey.__init__(self, to, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': form_fields.ChainedModelChoiceField,
            'queryset': self.rel.to._default_manager.complex_filter(self.rel.limit_choices_to),
            'to_field_name': self.rel.field_name,
            'app_name': self.app_name,
            'model_name': self.model_name,
            'mapp_name': self.mapp_name,
            'middle_name': self.middle_name,
            'chain_field': self.chain_field,
            'model_field': self.model_field,
            'show_all': self.show_all,
            'auto_choose': self.auto_choose,
        }
        defaults.update(kwargs)
        return super(ChainedForeignKey, self).formfield(**defaults)


class GroupedForeignKey(ForeignKey):
    """
    Opt Grouped Field
    """
    def __init__(self, to, group_field, **kwargs):
        self.group_field = group_field
        self._choices = True
        ForeignKey.__init__(self, to, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': form_fields.GroupedModelSelect,
            'queryset': self.rel.to._default_manager.complex_filter(self.rel.limit_choices_to),
            'to_field_name': self.rel.field_name,
            'order_field': self.group_field,
        }
        defaults.update(kwargs)
        return super(ForeignKey, self).formfield(**defaults)

if has_south:
    rules_grouped = [(
        (GroupedForeignKey,),
        [],
        {
            'to': ['rel.to', {}],
            'group_field': ['group_field', {}],
        },
    )]

    add_introspection_rules([], ["^smart_selects\.db_fields\.ChainedForeignKey"])
    add_introspection_rules(rules_grouped, ["^smart_selects\.db_fields\.GroupedForeignKey"])
