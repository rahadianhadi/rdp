from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from xapps.xname.models.xname import XModel
from xapps.xname.forms.xname import XModelForm

class XModelCreateView(CreateView):
    model = XModel
    form_class = XModelForm
    template_name = 'xname_form.html'
    success_url = reverse_lazy('xname-list')  # Redirect after successful submission
    