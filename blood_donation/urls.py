from django.urls import path
from .views import blood_donate_view, PostDetailView, reply_donation, add_blood_info, my_blood_info,\
    BloodInfoUpdateView, blood_donation_post, PostDelete, PostUpdateView, my_donation_post_list
app_name = 'blood_donation'

urlpatterns = [

    path('', blood_donate_view, name='blood-home'),
    path('add-blood-info/', add_blood_info, name='add-blood-info'),
    path('my-blood-detail/', my_blood_info, name='blood-info'),
    path('my-blood-detail/<slug:slug>/edit/', BloodInfoUpdateView.as_view(), name='info-update'),
    path('create-donation-post/', blood_donation_post, name='create-post'),
    path('<slug:slug>/detail/', PostDetailView.as_view(), name='post-detail'),
    path('<slug:slug>/update/', PostUpdateView.as_view(), name='post-update'),
    path('<slug:slug>/delete/', PostDelete.as_view(), name='post-delete'),
    path('my-post-list/', my_donation_post_list, name='my-post-list'),
    path('<slug:slug>/detail/reply/', reply_donation, name='post-reply'),
]


