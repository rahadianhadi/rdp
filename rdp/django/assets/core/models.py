from django.db import models

class BaseModel(models.Model):
  # Default
  created_at = models.DateTimeField(auto_now_add=True, blank=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  class Meta:
    abstract = True
  