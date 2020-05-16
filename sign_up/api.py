from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.mail import BadHeaderError, mail_admins
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .serializers import SignUpFormSerializer

class SignUpFormAPI(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = SignUpFormSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name    = serializer.validated_data['name']
        email   = serializer.validated_data['email']
        project = serializer.validated_data['project']
        message = serializer.validated_data['message']

        if name and email and project and message:
            subject = ' NEW CLIENT SIGNUP \u2014 {n}'.format(n=name)
            html_message = render_to_string('email.html', serializer.validated_data)
            plain_message = strip_tags(html_message)

            try:
                mail_admins(subject, plain_message, html_message=html_message)
            except BadHeaderError:
                return Response('Invalid header found.')
            return Response('Message sent successfully.')
        else:
            return Response('Make sure all fields are entered and valid.')

