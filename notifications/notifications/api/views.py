from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CredentialSerializer, ExamSerializer,NotificationSerializer
from .models import User, Notification, UserNotification
from .comunications import Mailer
from django.shortcuts import get_object_or_404

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
# Create your views here.

class SendCredentialAPIView(APIView):
    serializer_class = CredentialSerializer
    @swagger_auto_schema(
        operation_description="Sends credentials to a user identified by their ID",
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID of the user to send the credentials to", 
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        request_body=CredentialSerializer,
        responses={
            200: openapi.Response(
                description="Credentials Sent Successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            400: openapi.Response(
                description="Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_OBJECT),
                    },
                ),
            ),
            404: openapi.Response(
                description="User not found",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
        },
    )
    def post(self, request, id):
        #check the user exists
        email = User.objects.get_email(id)
        if email:
            serializer = self.serializer_class(data=request.data)
            # Validate the data
            if serializer.is_valid():
                # Access the validated data
                username = serializer.validated_data['username']
                password = serializer.validated_data['password']
                Mailer.send_credentials_email(email, username, password)
                return Response({'message': 'Credentials Sent'}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
        else:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
class SendExamDetailsAPIView(APIView):
    serializer_class = ExamSerializer
    @swagger_auto_schema(
        operation_description="Sends exam details and notifications to users",
        request_body=ExamSerializer,
        responses={
            200: openapi.Response(
                description="Notifications Sent Successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            400: openapi.Response(
                description="Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_OBJECT),
                    },
                ),
            ),
        },
    )
    def post(self, request):
        #check the user exists
        serializer = self.serializer_class(data=request.data)
        # Validate the data
        if serializer.is_valid():
            # Access the validated data
            userids,emails = zip(*serializer.validated_data['users'])
            examid,exam = serializer.validated_data['exam']
            UserNotification.objects.create_user_notification(userids,
                "Enrolled in exam",f"{exam['examUC']}", 
                f"You Were enrolled in exam: {exam['examName']}"+"\n"+
                f"Exam Date: {exam['examDate']}"+"\n"+
                f"Exam Time: {exam['examHour']}"
            )
            Mailer.send_exam_details_email(emails, exam)
            return Response({'message': 'Notifications Sent'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  


class SendExamAccessAPIView(APIView):
    serializer_class = ExamSerializer
    @swagger_auto_schema(
        operation_description="Sends exam access notifications to a teacher",
        request_body=ExamSerializer,
        responses={
            200: openapi.Response(
                description="Notifications Sent Successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            400: openapi.Response(
                description="Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_OBJECT),
                    },
                ),
            ),
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # Access the validated data
            userids,emails = zip(*serializer.validated_data['users'])
            examid,exam = serializer.validated_data['exam']
            UserNotification.objects.create_user_notification(userids,
                "Invited to exam",f"{exam['examUC']}",                                               
                f"You Were invited to an exam: {exam['examName']}")
            Mailer.send_exam_access_email(emails,exam)
            return Response({'message': 'Notifications Sent'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SendExamGradesAPIView(APIView):
    serializer_class = ExamSerializer
    @swagger_auto_schema(
        operation_description="Sends exam grades notifications to users",
        request_body=ExamSerializer,
        responses={
            200: openapi.Response(
                description="Notifications Sent Successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            400: openapi.Response(
                description="Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_OBJECT),
                    },
                ),
            ),
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # Access the validated data
            userids,emails = zip(*serializer.validated_data['users'])
            examid,exam = serializer.validated_data['exam']
            UserNotification.objects.create_user_notification(userids,
                "Grades published",f"{exam['examUC']}",
                f"The grades for the exam: {exam['examName']} where puslished")
            Mailer.send_grades_exam_email(emails,exam)
            return Response({'message': 'Notifications Sent'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SendExamRoomDeletedAPIView(APIView):
    serializer_class = ExamSerializer
    @swagger_auto_schema(
        operation_description="Sends notifications to teachers that the exam room is deleted for a specific subject",
        request_body=ExamSerializer,
        responses={
            200: openapi.Response(
                description="Notifications Sent Successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            400: openapi.Response(
                description="Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_OBJECT),
                    },
                ),
            ),
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # Access the validated data
            userids,emails = zip(*serializer.validated_data['users'])
            examid,exam = serializer.validated_data['exam']
            UserNotification.objects.create_user_notification(userids,
                "Room for exam deleted",f"{exam['examUC']}", 
                f"The room for the exam: {exam['examName']} was deleted")
            Mailer.send_exam_room_deleted_email(emails,exam)
            return Response({'message': 'Notifications Sent'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class getNotificationsAPIView(APIView):
    serializer_class = NotificationSerializer
    @swagger_auto_schema(
        operation_description="Gets notifications for a specific user ordered by most recent first",
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID of the user to get notifications for",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Notifications retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "unread":openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'message': openapi.Schema(type=openapi.TYPE_STRING),
                            'timestamp': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                        },
                    ),
                        "read":openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'message': openapi.Schema(type=openapi.TYPE_STRING),
                            'timestamp': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                        },
                    ),
                    }
                ),
            ),
            404: openapi.Response(
                description="User not found",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
        },
    )
    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        user_notifications_unread = UserNotification.objects.filter(user=user,is_read=False).order_by('-notification__timestamp')
        user_notifications_read = UserNotification.objects.filter(user=user,is_read=True).order_by('-notification__timestamp')
        serialized_notifications_unread = self.serializer_class([n.notification for n in user_notifications_unread], many=True)
        serialized_notifications_read = self.serializer_class([n.notification for n in user_notifications_read], many=True)
        for u in user_notifications_unread:
            u.is_read = True
            u.save()
        return Response({"unread":serialized_notifications_unread.data,"read":serialized_notifications_read.data}, status=status.HTTP_200_OK)