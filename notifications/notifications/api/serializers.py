from rest_framework import serializers
from .models import User,Notification

class IdFieldToEmail(serializers.UUIDField):
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        #Covert the id to email
        email = User.objects.get_email(data)
        if email:
            transformed_data = (data,email)
        else:
            raise serializers.ValidationError(f"There is no user with the id: {data}")
        return transformed_data
    
class IdFieldToExam(serializers.UUIDField):
    
    def get_exam(self, exam_id):
        try:
            """
            #TODO:: change this
            # Assuming your user API endpoint is at 'Exam/id/'
            response = requests.get(f'http://example.com/Exam/{user_id}/')  # Replace 'example.com' with your actual domain
            response.raise_for_status()  # Raise an exception for bad responses (4xx and 5xx)

            user_data = response.json()
            return user_data.get('idfk')
            """
            return {
                  "examName": "RAS - Exam number 1",
                  "examUC": "RAS",
                  "examDate": "16/12/2023",
                  "examHour": "16:00",
                  "examAdmissionTime": "00:15",
                  "examDuration": "02:30"
            }
        except requests.exceptions.RequestException as e:
            # Handle request errors (e.g., connection error, timeout)
            return None
    
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        #Covert the id to email
        exam = self.get_exam(data)
        if exam:
            transformed_data = (data,exam)
        else:
            raise serializers.ValidationError(f"There is no exam with the id: {data}")
        return transformed_data




class CredentialSerializer(serializers.Serializer):
    username = serializers.CharField(help_text="Username of student")
    password = serializers.CharField(help_text="Password of student")

class ExamSerializer(serializers.Serializer):
    users = serializers.ListField(child=IdFieldToEmail(),help_text="List of students IDs")
    exam = IdFieldToExam(help_text="Id of exam")

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['message','timestamp']