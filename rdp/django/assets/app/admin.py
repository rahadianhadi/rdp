from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from xapps.xname.models.xname import XModel


class XModelResource(resources.ModelResource):
    class Meta:
        model = XModel
        fields = ('id', 'name', 'created_at', 'updated_at')  # Add fields you want to export/import
        export_order = ('id', 'name', 'created_at', 'updated_at')


class XModelAdmin(ImportExportModelAdmin):
    # Search configuration
    search_fields = ('name', )  # Search by name or description

    # List display configuration
    list_display = ('id', 'name', 'created_at', 'updated_at')

      # Sort configuration
    ordering = ('-created_at',)  # Sort by creation date in descending order


    # Pagination configuration
    list_per_page = 20  # Adjust the number of items per page

    # Import/Export functionality
    resource_class = XModelResource

    # Additional configurations can be added here for fields, actions, etc.
    
    # Optionally, enable inlines, actions, or readonly fields:
    # inlines = [XModelInline]
    # actions = ['make_featured']
    
    # Filter configuration
    # list_filter = ('category', 'price')  # Filter by category and price

    
    # def make_featured(self, request, queryset):
    #     # Custom action to mark XModels as featured, for example
    #     queryset.update(is_featured=True)
    # make_featured.short_description = "Mark selected XModels as featured"


# Register the XModel model with the custom admin class
admin.site.register(XModel, XModelAdmin)
