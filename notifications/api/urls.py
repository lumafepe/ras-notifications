from django.urls import path
from .views import SendCredentialAPIView,SendExamDetailsAPIView,SendExamAccessAPIView,SendExamGradesAPIView,SendExamRoomDeletedAPIView,getNotificationsAPIView
from .consumers import NotificationConsumer
urlpatterns = [
    path('credentials/<id>/', SendCredentialAPIView.as_view(), name='credentials'),
    path('exam/details/', SendExamDetailsAPIView.as_view(), name='exam_details'),
    path('exam/access/', SendExamAccessAPIView.as_view(), name='exam_access'),
    path('exam/grades/', SendExamGradesAPIView.as_view(), name='exam_grades'),
    path('exam/roomDeleted/', SendExamRoomDeletedAPIView.as_view(), name='exam_room_deleted'),
    path('<id>/', getNotificationsAPIView.as_view(), name='list'),
    path(r'ws/<user_id>', NotificationConsumer.as_asgi())
]
