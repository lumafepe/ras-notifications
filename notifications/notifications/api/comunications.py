from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

class Mailer():
    @staticmethod
    def send_email(emails,subject,template_name,context):
        html_message = render_to_string(template_name, context)
        send_mail(
            subject=subject,
            message='',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=emails,
            html_message=html_message
        )
    @staticmethod
    def send_credentials_email(email,username,password):
        #html template to send
        template_name = 'credentials.html'
        #Data to fill the template
        context = {
            'username': username, 
            'password': password
        }
        #Render the template with the data
        
        
        Mailer.send_email(
            emails=[email],
            subject="PROBUM:: Credentials",
            template_name=template_name,
            context=context
        )
        
    @staticmethod
    def send_exam_details_email(emails,exam):
        #html template to send
        template_name = 'exam_details.html'
        #Data to fill the template
        context = exam
        #Render the template with the data
        

        Mailer.send_email(
            emails=emails,
            subject="PROBUM:: New Exam details",
            template_name=template_name,
            context=context
        )
    @staticmethod
    def send_exam_access_email(emails,exam):
        #html template to send
        template_name = 'exam_access.html'
        #Data to fill the template
        context = exam
        #Render the template with the data
        
        Mailer.send_email(
            emails=emails,
            subject="PROBUM:: New Exam Access",
            template_name=template_name,
            context=context
        )
    @staticmethod
    def send_grades_exam_email(emails,exam):
        #html template to send
        template_name = 'exam_grades.html'
        #Data to fill the template
        context = exam
        #Render the template with the data
        
        Mailer.send_email(
            emails=emails,
            subject="PROBUM:: New Grades",
            template_name=template_name,
            context=context
        )
    @staticmethod
    def send_exam_room_deleted_email(emails,exam):
        #html template to send
        template_name = 'exam_room_deleted.html'
        #Data to fill the template
        context = exam
        #Render the template with the data
        

        Mailer.send_email(
            emails=emails,
            subject="PROBUM:: Exam room deleted",
            template_name=template_name,
            context=context
        )