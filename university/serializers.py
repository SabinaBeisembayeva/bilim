from rest_framework import serializers
from school.models import SubjectFirst
from university.admin import UserPassPointAdmin

from university.models import Specialty, Stuff, University, Faculty, GrantPoint, UniversityPassPoint, UserPassPoint


class UniversitySerializer(serializers.ModelSerializer):

    class Meta:
        model = University
        fields = ['id', 'title', 'address', 'image']


class SpecialtyDetailedSerializer(serializers.ModelSerializer):
    faculty = serializers.SerializerMethodField()
    grant_point = serializers.SerializerMethodField()
    subject_one = serializers.SerializerMethodField()
    subject_two = serializers.SerializerMethodField()
    stuff = serializers.SerializerMethodField()

    class Meta:
        model = Specialty
        fields = ['id', 'title', 'faculty', 'grant_point',
                   'subject_one', 'subject_two', 'stuff']

    def get_faculty(self, obj):
        return obj.faculty.title

    def get_grant_point(self, obj):
        grant = GrantPoint.objects.get(specialty=obj)
        return grant.point
    
    def get_subject_one(self, obj):
        subject_one = GrantPoint.objects.get(specialty=obj)
        return subject_one.subject_first.title
    
    def get_subject_two(self, obj):
        subject_two = GrantPoint.objects.get(specialty=obj)
        return subject_two.subject_second.title
    
    def get_stuff(self, obj):
        stuff = Stuff.objects.filter(faculty=obj.faculty).first()
        return stuff.bio


class SpecialtySerializer(serializers.ModelSerializer):
    faculty = serializers.SerializerMethodField()
    grant_point = serializers.SerializerMethodField()
    class Meta:
        model = Specialty
        fields = ['id', 'title', 'faculty', 'grant_point']

    def get_faculty(self, obj):
        return obj.faculty.title

    def get_grant_point(self, obj):
        grant = GrantPoint.objects.get(specialty=obj)
        return grant.point


class SpecialtyWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Specialty
        fields = ['id', 'title']


class UniversityDetailedSerializer(serializers.ModelSerializer):
    specialty = serializers.SerializerMethodField('get_specialty')
    city = serializers.SerializerMethodField()

    class Meta:
        model = University
        fields = ['id', 'title', 'city', 'image', 'specialty']

    def get_city(self, obj):
        return obj.city.title

    def get_specialty(self, obj):
        faculties = Faculty.objects.filter(university=obj).values_list('id', flat=True)
        specialties = Specialty.objects.filter(faculty__in=faculties)
        serializer = SpecialtySerializer(specialties, many=True)
        return serializer.data

class UniversityDetailedReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = University
        fields = '__all__'

class FacultySerializer(serializers.ModelSerializer):

    class Meta:
        model = Faculty
        fields = ['id', 'title']



class ReadSpecialtySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    title = serializers.CharField()    


class DetailedFacultySerializer(serializers.ModelSerializer):

    specialty = SpecialtySerializer(many=True, read_only=True)

    class Meta:
        model = Faculty
        fields = ['id', 'title', 'specialty']
    
class DetailedReadFacultySerializer(serializers.ModelSerializer):

    specialty = serializers.SerializerMethodField()

    class Meta:
        model = Faculty
        fields = ['id', 'title', 'specialty']
    
    def get_specialty(self, obj):
        data = []
        specialty = Specialty.objects.filter(faculty_id=obj.id)
        for spec in specialty:
            context = {
                "id": spec.id,
                "title": spec.title
            }
            data.append(context)
        return data

class DetailedUniversitySerializer(serializers.ModelSerializer):
    pass
    
class MotivationSerialzier(serializers.Serializer):
    quote = serializers.CharField()

class UserPassPointSerializer(serializers.ModelSerializer):
    university = UniversitySerializer(read_only=True)
    faculty = FacultySerializer(read_only=True)
    specialty = SpecialtyWriteSerializer(read_only=True)

    class Meta:
        model = UserPassPoint
        fields = ['id', 'university', 'faculty', 'specialty', 'result']


class UniversityPassPointSerializer(serializers.ModelSerializer):
    university = UniversitySerializer(read_only=True)
    faculty = FacultySerializer(read_only=True)
    specialty = SpecialtyWriteSerializer(read_only=True)

    class Meta:
        model = UniversityPassPoint
        fields = ['id', 'university', 'faculty', 'specialty', 'pass_point']
