"""
URL configuration for store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/',views.base),
    path('register/',views.register),
    path('',views.body),
    
    path('filterbycategory/<cat>/',views.filterbycategory),
    path('sortbyprice/<p>/',views.sortbyprice),
    path('filterbyprice/',views.filterbyprice),
    # discount filter url
    path('products/', views.product_list, name='product_list'),
  
    path('addtocart/<pid>/',views.addtocart),
    path('mycart/',views.viewcart),
    path('shopmore',views.shopmore),
    path('removecart/<cid>/',views.removecart),
    path('updateqty/<x>/<cid>/',views.updateqty),
    path('checkaddress/',views.checkaddress),
    path('back/',views.back),
    path('placeorder/',views.placeorder),
    #path('placeorder/', views.placeorder, name='placeorder'),
    path('fetchorder/',views.fetchorder),
    path('login/',views.ulogin),
    path('logout/',views.ulogout),
    path('product_details/<pid>/',views.product_details),
    #path('makepayment/',views.makepayment),
    path('email_send/',views.email_send),
    path('update_order_status/',views.update_order_status),
    path('discount_percentage/',views.discount_percentage),
    path('makepayment/', views.makepayment, name='makepayment'),

    path('my_order/', views.my_order, name='my_order'),

    path("bmi/", views.bmi_calculator, name="bmi_calculator"),
    path('build_muscle/',views.build_muscle),
    path('lean_muscle/',views.lean_muscle),
    path('fat_loss/',views.fat_loss),
    path('exercise/',views.exercise),
    path('contact/', views.contact_page, name='contact'),
    

#forget password

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)