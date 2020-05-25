from re import search
from html import escape
from rest_framework.serializers import Serializer, CharField, ValidationError

class SignUpFormSerializer(Serializer):
    name    = CharField()
    email   = CharField()
    project = CharField()
    message = CharField()

    def get_email_regex(self):
        return '^[a-zA-Z0-9_+&*-]+(?:\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,7}$'

    def get_project_options(self):
        return [
            'Wedding, entertainment, or special event',
            'Commercial or promotional work',
            'Documentary or artistic project',
            'Other'
        ]

    def validate_name(self, name):
        test = escape(name)
        if test is not name:
            raise ValidationError('Invalid name provided.')
        return test.strip()

    def validate_email(self, email):
        test = escape(email, quote=True)
        if test is not email or not search(self.get_email_regex(), email):
            raise ValidationError('Invalid email address provided.')
        return test.strip()

    def validate_project(self, project):
        test = escape(project, quote=True)
        if test is not project or project not in self.get_project_options():
            raise ValidationError('Invalid project selected.')
        return test.strip()

    def validate_message(self, message):
        message = message.strip()
        if not message:
            raise ValidationError('Invalid message.')
        return escape(message)
