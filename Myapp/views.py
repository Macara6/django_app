



from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics, permissions
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework.generics import DestroyAPIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework.generics import UpdateAPIView

from datetime import datetime, timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from .models import *


class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request,*args, **kwargs):
        serializers = TokenRefreshSerializer(data = request.data)
        serializers.is_valid(raise_exception= True)

        new_token = serializers.validated_data['access']

        return Response({
            'token': new_token
        }, status= status.HTTP_200_OK)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        passward = request.data.get('password')
        user = authenticate(request, username=username, password=passward)
        
        if user is not None:
           
            token = RefreshToken.for_user(user)

            return Response ({
            'id':user.id,
            'username':user.username,
            'email':user.email,
            'token':str(token.access_token  ) 
        }, status = status.HTTP_200_OK)
        
        else:
            return Response({'error':'Compte non trouvé ou identifiants invalides'}, status=status.HTTP_401_UNAUTHORIZED)
        
class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request,*args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            return Response({
                'id':user.id,
                'username': user.username,
                'email': user.email,
                'message':'User created successfully'
            }, status = status.HTTP_201_CREATED )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post (self , request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not old_password or not new_password:
            return Response({'error':' Les deux champs sont requis'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(old_password):
            return Response({'error':'Ancien mot de pass incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({'message': 'Mot de passe modifié avec succès.'}, status=status.HTTP_200_OK)
    

class UserView(generics.ListAPIView):
     queryset =  User.objects.all()
     serializer_class = UserViewSerializer

class DeleteUserView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field ='pk' 

      
class CategoryView(generics.ListAPIView):
    queryset= Category.objects.all()
    serializer_class = CategoryViewSerializer    



class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class =  ProductCreateSerializer
    permission_classes = [IsAuthenticated]

class BureauCreateView(generics.CreateAPIView):
    queryset = Bureau.objects.all()
    serializer_class = BureauCreateSerializer
    permission_classes =[IsAuthenticated] 
    

class BureauView(generics.ListAPIView):
    queryset = Bureau.objects.all()
    serializer_class= BureauCreateSerializer
    permission_classes = [IsAuthenticated]  

class BureauDetailView(generics.RetrieveUpdateAPIView):
    queryset = Bureau.objects.all()
    serializer_class = BureauCreateSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        partial = True
        return self.update(request, *args, **kwargs)

class DeleteBureauView(DestroyAPIView):
    queryset = Bureau.objects.all()
    serializer_class = BureauCreateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field='pk'

#APi pour user profil 
class UserProfilView(generics.ListAPIView):
        serializer_class = UserProfilViewSerializer
        def get_queryset(self):
            querset = UserProfile.objects.all()
            user_id = self.request.query_params.get('user')
            if user_id is not None:
                querset = querset.filter(user= user_id)
                return querset
            
#API pour la modification du profil
class UserProfilUpdateView(generics.UpdateAPIView):
     queryset = UserProfile.objects.all()
     serializer_class = UserProfilViewSerializer
     permission_classes = [IsAuthenticated]

     def get_object(self):
        user_profil = UserProfile.objects.get(user = self.queryset.user)
        return  user_profil

     def perform_update(self, serializer):
        serializer.save(user = self.request.user)
#fin de la fonction            

class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
       queryset = Product.objects.all().order_by('-created_at')
       return queryset


class ProductDetailView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        partial = True
        return self.update(request, *args, **kwargs)
    
    def delete( self, request, *args, **kwargs):
        instance =self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class CashOutView(generics.ListAPIView):
        serializer_class = CashOutSerializer
        permission_classes = [IsAuthenticated]

        def get_queryset(self):
            queryset = CashOut.objects.all().order_by('-created_at')

            return queryset

   
class CashOutDetailView(generics.ListAPIView):
    serializer_class = CashOutDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cashout_id = self.request.query_params.get('cashout')

        if cashout_id:
            return CashOutDetail.objects.filter(cashout__id = cashout_id)
        
        return  CashOutDetail.objects.none()

class CreateCashOutView(generics.CreateAPIView):
    queryset = CashOut.objects.all()
    serializer_class = CashOutCreateSerializer
    permission_classes = [IsAuthenticated]
    

class CreateDeliveryNoteView(generics.CreateAPIView):
    queryset = DeliveryNote.objects.all()
    serializer_class = DeliveryNoteCreateSerializer
    permission_classes = [IsAuthenticated]

class DeliveryNoteListView(generics.ListAPIView):
    queryset = DeliveryNote.objects.all().order_by('-created_at')
    serializer_class = DeliveryNoteListViewSerializer
    permission_classes = [IsAuthenticated]

class DeliveryNoteDetailView(generics.ListAPIView):
    queryset = DeliveryNoteItem.objects.all()
    serializer_class = DeliveryNoteDetailViewSerializer

    def get_queryset(self):
        delivery_note_id = self.kwargs.get('pk')
        if delivery_note_id:
            return DeliveryNoteItem.objects.filter(delivery_note_id=delivery_note_id)
        
        return DeliveryNoteItem.objects.none()
    
class DeleteDeliveryNoteView(DestroyAPIView):
    queryset = DeliveryNote.objects.all()
    serializer_class = DeliveryNoteCreateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'


class DeleteCashOutView(DestroyAPIView):
        queryset = CashOut.objects.all()
        serializer_class = CashOutCreateSerializer
        permission_classes = [IsAuthenticated]
        lookup_field='pk'

class CreatePDFdocument(generics.CreateAPIView):
    queryset = PDFDocument.objects.all()
    serializer_class = PDFDocumentCreateSerializer
    permission_classes = [IsAuthenticated]

    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DeletePDFDocument(DestroyAPIView):
    queryset = PDFDocument.objects.all()
    serializer_class = PDFDocumentCreateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field ='pk'

class PDFDocumentsViewList(generics.ListAPIView):
    serializer_class = PDFDocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = PDFDocument.objects.all().order_by('-created_at')
        return queryset


class PDFDocumentDetailView(generics.RetrieveAPIView):
    queryset = PDFDocument.objects.all()
    serializer_class = PDFDocumentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field ='pk' 
