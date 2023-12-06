from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.landing, name ='landing'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('login/main',views.main, name='main'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/main/creation',views.art_creation, name='creation'),
    path('register/',views.register, name='register'),
    path('login/main/author', views.author, name='author'),
    path('login/main/new_deal', views.deals_Creation, name='deals'),
    path('login/main/account', views.account, name='account'),

    #Paypal URLS
    path('paypal-return', views.paypal_return, name ='paypal-return'),
    path('paypal-cancel', views.paypal_cancel, name ='paypal-cancel'),
    path('', views.landing, name ='landing'),

    # TEST URLS
    path('photo/', include('photo.urls')),
]
