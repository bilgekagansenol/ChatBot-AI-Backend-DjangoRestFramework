from rest_framework import viewsets , permissions
from rest_framework import filters

from promptbox_api.models import PromptBoxItem

from promptbox_api.serializers import PromptBoxItemSerializer



class PromptBoxItemViewSet(viewsets.ModelViewSet):
    """viewset for creating , listing and managing promptbox items"""
    serializer_class = PromptBoxItemSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['PromptBoxItem_information']
    queryset = PromptBoxItem.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    

    def get_queryset(self):
        """returns promptbox that belongs  who is authenticated"""
        return self.queryset.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """add  user automatically when creating new item"""
        serializer.save(user=self.request.user)
        
##try