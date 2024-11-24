from rest_framework import generics, filters
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from apps.core.api_paging import ApiPagination
from apps.xmodel.models.xmodel import XModel
from apps.xmodel.api.serializers import XModelSerializer

class XModelListCreate(generics.ListCreateAPIView):
    queryset = XModel.objects.all()
    serializer_class = XModelSerializer
    
    # Auth
    permission_classes = [IsAuthenticated]
    
    # GET /api/xmodel/?name=Phone
    filter_backends = [DjangoFilterBackend, SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'created_at']
    
    # GET /api/xmodel/?search=Smartphone
    search_fields = ['name']
    
    # Ordering
    # GET /api/xmodel/?ordering=name
    ordering_fields = ['name', 'created_at', ]  # Field yang bisa diurutkan '__all__' #
    ordering = ['-updated_at', ] 
    
    pagination_class = ApiPagination
    
    # GET /api/xmodel/?all=true
    def get(self, request, *args, **kwargs):
        # Check if the 'all' parameter is present in the query params
        if request.query_params.get('all'):
            # Return all items (without pagination)
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        # Otherwise, use the default paginated response
        return super().get(request, *args, **kwargs)

class XModelRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = XModelSerializer
  permission_classes = [IsAuthenticated]
  queryset = XModel.objects.all()
