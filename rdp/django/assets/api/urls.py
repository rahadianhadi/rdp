from django.urls import path
from .views.xmodel import XModelListCreate, XModelRetrieveUpdateDestroy

urlpatterns = [
  path('', XModelListCreate.as_view(), name='list-create'),
  path('<int:pk>/', XModelRetrieveUpdateDestroy.as_view(), name='retrieve-update-destroy')
]