from django import forms
from xapps.xname.models.xname import XModel

class XModelForm(forms.ModelForm):
    class Meta:
        model = XModel
        fields = ['name']  # Include fields to be displayed in the form
        # widgets = {
        #     'name': forms.TextInput(attrs={
        #         'class': 'form-control',
        #         'placeholder': 'Enter XModel name'
        #     })
        # }
        # labels = {
        #     'name': 'XModel Name'
        # }

    # Custom field validation for 'name'
    # def clean_name(self):
    #     name = self.cleaned_data.get('name')
    #     if not name:
    #         raise forms.ValidationError("The name field cannot be empty.")
    #     if len(name) < 3:
    #         raise forms.ValidationError("The xmodel name must be at least 3 characters long.")
    #     if XModel.objects.filter(name=name).exists():
    #         raise forms.ValidationError("A xmodel with this name already exists.")
    #     return name
