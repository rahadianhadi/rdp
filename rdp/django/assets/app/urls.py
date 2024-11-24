from django.urls import path
from .views.x_name import XModelView

urlpatterns = [
    path('', XModelView.as_view(), name='x_name'),
  ]
