from django.db import models
from x_apps.core.models import BaseModel

'''
Xmodel model
'''
class Xmodel(BaseModel):
  name = models.CharField(max_length=100)
  
  def __str__(self):
    return f'{self.name}'
  
  class Meta:
    verbose_name = 'Xmodel'
    db_table = 'x_model'
    ordering = ('-created_at', )