from audioop import error

from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from quickstart.models import Person
from quickstart.serializers import PersonSerializer


# Create your views here.
class PersonPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


# Create your views here.
# This class is responsible for handling the GET request for the Person model
class PersonAPIView(APIView):
    pagination_class = PersonPagination

    def get(self, request, *args, **kwargs):

        # get person by id
        id = kwargs.get('id', None)
        if id is not None:
            person = get_object_or_404(Person, id=id)
            serializer = PersonSerializer(person)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:

            # get all the data from the Person model
            persons = Person.objects.all()
            if not persons.exists():
                return Response({"message": "No Person found"}, status=status.HTTP_404_NOT_FOUND)

        # Check for 'Ordering' query parameter
        ordering = request.query_params.get('ordering', None)
        if ordering is not None:
            persons = persons.order_by(ordering)

        # Filtering the data based on the query parameters
        first_name = request.query_params.get('first_name', None)
        last_name = request.query_params.get('last_name', None)
        # If the query parameters are present, filter the data
        if first_name is not None:
            persons = persons.filter(first_name__contains=first_name)
        if last_name is not None:
            persons = persons.filter(last_name__contains=last_name)

        # Pagination of the data
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(persons, request)
        if page is not None:
            if len(page) == 0:
                return Response({"message": "No data found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = PersonSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        """
        Further improvements Task for future:
        1.	Advanced Filtering: Implement more complex filtering options, such as filtering by a combination of fields (e.g., by both first_name and last_name).
	    2.	Default Ordering: Consider setting a default ordering if none is specified. This can help ensure consistent results.
	    3.	Error Handling for Invalid Query Parameters: Extend your error handling to check for invalid ordering values or invalid query parameter formats.
	    4.	Rate Limiting: Implement rate limiting to prevent abuse of the API by limiting the number of requests a client can make in a given time period.
	    5.	Caching: Consider implementing caching for frequently accessed data to improve performance.
        """

        # Serialize the data and return it
        serializer = PersonSerializer(persons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        # Validate the data from the request
        errors = {}

        # # Validate the first and last name fields
        for field in ['first_name', 'last_name']:
            # Check if the field is present in the data and is not empty
            if field not in data or not data[field]:
                errors[field] = [f'{field.capitalize()} is required']
            # Check if the field contains only alphabets
            elif not data[field].isalpha():
                errors[field] = [f'{field.capitalize()} should contain only alphabets']
            # Check First Letter is Capital
            elif not data[field][0].isupper():
                errors[field] = [f'{field.capitalize()} should start with a capital letter']

        # If there are any errors, return the errors and a 400 Bad Request status
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        # Create a serializer instance with the data from the request
        serializer = PersonSerializer(data=request.data)

        # Check if the serializer has valid data
        if serializer.is_valid():
            # Save the new Person from the validated data
            person = serializer.save()

            # Return the serialized Person data and a 201 Created status
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # If data is invalid, return the errors and a 400 Bad Request status
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        # # Retrieve the Person object by id
        # id = kwargs.get('id', None)
        # # Check if the id is present in the URL
        # if id is not None:
        #     person = get_object_or_404(Person, id=id)
        #     serializer = PersonSerializer(person, data=request.data, partial=True)
        #     # Check if the serializer has valid data
        #     if serializer.is_valid():
        #         serializer.save()
        #         return Response(serializer.data, status=status.HTTP_200_OK)
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # # If the id is not present in the URL, return a 400 Bad Request status
        # return Response({"message": "Please Enter the ID in the URL Followed by Slash"}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the Person object by id
        person_id = kwargs.get('id', None)
        if person_id is None:
            return Response({"message": "ID is required in the URL"}, status=status.HTTP_400_BAD_REQUEST)

        person = get_object_or_404(Person, id=person_id)

        try:
            serializer = PersonSerializer(person, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Person Updated Successfully", "data": serializer.data},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except error:
            return Response({"message": "Error while updating the Person"}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        # Retrieve the Person object by id
        person_id = kwargs.get('id', None)
        if person_id is None:
            return Response({"message": "ID is required in the URL"}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the Person object by id
        person = get_object_or_404(Person, id=person_id)

        # Update the Person object with the data from the request
        try:
            serializer = PersonSerializer(person, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Person Updated Successfully", "data": serializer.data},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except error:
            return Response({"message": "Error while updating the Person"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        # Retrieve the Person object by id
        person_id = kwargs.get('id', None)
        if person_id is None:
            return Response({"message": "ID is required in the URL"}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the Person object by id
        person = get_object_or_404(Person, id=person_id)

        # Delete the Person object
        try:
            person.delete()
            return Response({"message": "Person Deleted Successfully"}, status=status.HTTP_200_OK)
        except error:
            return Response({"message": "Error while deleting the Person"}, status=status.HTTP_400_BAD_REQUEST)
