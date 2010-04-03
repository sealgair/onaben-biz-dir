"""
"""
from django import forms
from django import template

class NestedFormWidget(forms.widgets.Widget):
    """
    """
    
    def render(self):
        """
        """
        t = template.loader.get_template('formset_ul.html')
        c = template.Context({'formset': self})
        return t.render(c)

class NestedFormsetField(forms.fields.Field):
    """
    """
    
    def __init__(self, model, *args, **kwargs):
        """
        """
        self.model_class = model
    
    def clean(self, value):
        """
        """
        if len([d for d in value if len(d) > 0]) < self.min_num:
            raise forms.ValidationError("%s or more %s required" % (self.min_num, self.prefix))
        
        return super(NestedFormsetField, self).clean()

class NestableModelForm(forms.ModelForm):
    """
    Special ModelForm that can accept NestedFormsetField fields, and save them
    """
    
    def __init__(self, *args, **kwargs):
        """
        """
        self.formsets = {}
        inlines = [field.model_class for field in self.fields if isinstance(field, NestedFormsetField)]
        for formset_class in inlines:
            prefix = formset_class.get_default_prefix()
            self.formsets[prefix] = formset_class(prefix=prefix, *args, **kwargs)
        return super(NestableModelForm, self).__init__(*args, **kwargs)
        
    def save(self, *args, **kwargs):
        """
        """
        instance = super(NestableModelForm, self).save(*args, **kwargs)
        
        for formset in self.formsets.values():
            formset.instance = instance
            formset.save(*args, **kwargs)
        
        return instance
