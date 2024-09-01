from rest_framework import serializers

from .models import Person


# class PersonalInfoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PersonalInfo
#         fields = "__all__"


class PersonSerializer(serializers.ModelSerializer):
    # personal_info = PersonalInfoSerializer()

    class Meta:
        model = Person
        fields = "__all__"
