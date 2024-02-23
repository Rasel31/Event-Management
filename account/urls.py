from django.urls import path
from .views import event_approval_list, EventApproveView, SignUpView, ModeratorSignUpView, SecretarySignUpView

app_name = 'account'

urlpatterns = [
    path('event-approval-list/', event_approval_list, name='approval-list'),
    path('event-approval-list/<slug:slug>/approve/', EventApproveView.as_view(), name='approve-event'),
    path('head/register/', SignUpView.as_view(), name='head-register'),
    path('head/register/moderator/', ModeratorSignUpView.as_view(), name='head-register-moderator'),
    path('head/register/secretary/', SecretarySignUpView.as_view(), name='head-register-secretary'),

    path('moderator/register/secretary/', SecretarySignUpView.as_view(), name='moderator-register-secretary'),

]


