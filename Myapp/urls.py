from django.urls import path
from django.conf.urls.static import static
from.views import *

urlpatterns = [
    path('login/',LoginView.as_view(), name='login'),
    path('products/', ProductListView.as_view(), name='products'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
  
    path('usersView/', UserView.as_view(), name='user-list'),
    path('category/',CategoryView.as_view(), name='category-list'),
    path('productCreate/',ProductCreateView.as_view(), name='product-create'),
    path('userCreate/', UserCreateView.as_view(), name='user-create'),
    
    path('user/delete/<int:pk>/', DeleteUserView.as_view(), name='delete-user'),
    path('user/change-password/', ChangePasswordView.as_view(), name='change-password'),
   
    path('usersView/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('refresh-token/', CustomTokenRefreshView.as_view(), name='token_refresh'),
 
    path('userProfil/', UserProfilView.as_view(), name='user_profil'),
    path('userProfil/update/', UserProfilUpdateView.as_view(), name='user_profil_update'),
    #API pour le casout
    path('cashouts/', CashOutView.as_view(), name='cashout-list'),
    path('cashoutDetail/', CashOutDetailView.as_view(), name='cashout-detail'),
    path('cashout/create/', CreateCashOutView.as_view(), name='create-cashout'),

    path('bureauxCreate/', BureauCreateView.as_view(), name='bureau-create'),
    path('bureaux/', BureauView.as_view(), name='bureau-view'),
    path('bureau/delete/<int:pk>/',DeleteBureauView.as_view(), name='delete-bureau'),
    path('bureau/update/<int:pk>/', BureauDetailView.as_view(), name='update-bureau'),

    path('delivery-note/create/', CreateDeliveryNoteView.as_view(), name='create_delivery_note'),
    path('delivery-notes/',DeliveryNoteListView.as_view(), name='list_delivery'),

    path('delivery-note-detail/<int:pk>/items/', DeliveryNoteDetailView.as_view(), name='delivery-note-detail'),
        #api pour supprimet le bon de livrasion et bon de sortie 
    path('delivery-note/delete/<int:pk>/', DeleteDeliveryNoteView.as_view(), name='delete-delivery'),
    path('cashout/delete/<int:pk>/', DeleteCashOutView.as_view(), name='delete_cashout'),

    path('PdfDocumentsList/', PDFDocumentsViewList.as_view(), name='PDFDocumentsList'),
    path('PdfDocument/<int:pk>/',PDFDocumentDetailView.as_view(), name='pdf-detail'),
    path('PdfDocument/create/', CreatePDFdocument.as_view(), name = 'creat_pdf'),
    path('PdfDocument/delete/<int:pk>/',DeletePDFDocument.as_view(), name='delete_pdf')
   
    

   

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
