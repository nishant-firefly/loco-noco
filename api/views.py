from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
import pandas as pd
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import User, Role, EntityRolePermission
from .serializers import UserSerializer, RoleSerializer, EntityRolePermissionSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def upload_excel(self, request):
        if 'file' not in request.FILES:
            return Response({"error": "No file provided"}, status=400)

        file = request.FILES['file']
        df = pd.read_excel(file)
        return JsonResponse(df.to_dict())

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]

class EntityRolePermissionViewSet(viewsets.ModelViewSet):
    queryset = EntityRolePermission.objects.all()
    serializer_class = EntityRolePermissionSerializer
    permission_classes = [IsAuthenticated]

# ✅ Add SomeProtectedView here
class SomeProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "You have access to this protected endpoint!"}, status=200)





# from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.decorators import action
# from rest_framework.response import Response
# import pandas as pd
# from django.http import JsonResponse
# from .models import User, Role, EntityRolePermission
# from .serializers import UserSerializer, RoleSerializer, EntityRolePermissionSerializer








# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]


#     @action(detail=False, methods=['post'])
#     def upload_excel(self, request):
#         if 'file' not in request.FILES:
#             return Response({"error": "No file provided"}, status=400)

#         file = request.FILES['file']
#         df = pd.read_excel(file)
#         return JsonResponse(df.to_dict())

    
# class RoleViewSet(viewsets.ModelViewSet):
#     queryset = Role.objects.all()
#     serializer_class = RoleSerializer
#     permission_classes = [IsAuthenticated]

# class EntityRolePermissionViewSet(viewsets.ModelViewSet):
#     queryset = EntityRolePermission.objects.all()
#     serializer_class = EntityRolePermissionSerializer
#     permission_classes = [IsAuthenticated]





