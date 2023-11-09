from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path('',views.Offer.as_view()),
    path('myoffer/',views.Myoffer),
    path('<int:off_id>/',views.Offer.as_view()),
    path('create_user/',views.UserDetailAPI.as_view()),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(), name='token_refresh'),
]

