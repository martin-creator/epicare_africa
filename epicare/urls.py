from django.urls import path
from epicare import views


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('about/', views.about, name='about'),
    path('shop/', views.shop, name='shop'),
    path('shop/buy/<int:product_id>/', views.buy_now, name='buy_now'),
    path('blog/', views.blog, name='blog'),
    path('blog/<int:post_id>/', views.blog_detail, name='blog_detail'),
    path('contact/', views.contact, name='contact'),
    path('careers/', views.careers, name='careers'),
    path('admin/export-newsletter-csv/', views.export_newsletter_csv, name='export_newsletter_csv'),
] 