import re
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

    def validate_email(self, email):
        if (re.search(self.get_email_regex(), email) == None):
            raise ValidationError('Invalid email address provided.')
        return email

    def validate_project(self, project):
        if (project not in self.get_project_options()):
            raise ValidationError('Invalid project selected.')
        return project
