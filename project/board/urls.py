from django.urls import path

from .views import announcement_list, AnnouncementDetail, AnnouncementCreate, AnnouncementEdit, AnnouncementDelete, \
    CreateResponse, ResponseList, ResponseDelete, accept_response, NewsCreate

urlpatterns = [
    path('', announcement_list, name='announcement_list'),
    path('<int:pk>/', AnnouncementDetail.as_view(), name='announcement_detail'),
    path('create/', AnnouncementCreate.as_view(), name='announcement_create'),
    path('<int:pk>/edit/', AnnouncementEdit.as_view(), name='announcement_edit'),
    path('<int:pk>/delete/', AnnouncementDelete.as_view(), name='announcement_delete'),
    path('<int:pk>/create_response/', CreateResponse.as_view(), name='response_create'),
    path('responses/', ResponseList.as_view(), name='response_list'),
    path('<int:pk>/delete-resp', ResponseDelete.as_view(), name='response_delete'),
    path('<int:pk>/accept-resp', accept_response, name='response_accept'),
    path('news-create/', NewsCreate.as_view(), name='news_create')
]
