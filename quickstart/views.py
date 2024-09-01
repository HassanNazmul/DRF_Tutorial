from rest_framework import viewsets, status
from rest_framework.response import Response

from quickstart.models import Person, PersonalInfo
from quickstart.serializers import PersonSerializer


# Create your views here.
class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def create(self, request, *args, **kwargs):
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")

        # Extract nested personal_info data
        personal_info_data = request.data.get("personal_info", {})
        age = personal_info_data.get("age")
        job = personal_info_data.get("job")

        # Create the Person instance
        person = Person.objects.create(first_name=first_name, last_name=last_name)

        # Create the associated PersonalInfo instance
        PersonalInfo.objects.create(person=person, age=age, job=job)

        return Response(PersonSerializer(person).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Extract nested data
        personal_info_data = request.data.get('personal_info')

        # Update Person fields
        instance.first_name = request.data.get('first_name', instance.first_name)
        instance.last_name = request.data.get('last_name', instance.last_name)
        instance.save()

        # Update or create PersonalInfo
        if personal_info_data:
            personal_info_instance = instance.personal_info
            personal_info_instance.age = personal_info_data.get('age', personal_info_instance.age)
            personal_info_instance.job = personal_info_data.get('job', personal_info_instance.job)
            personal_info_instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
