from django.db.models import query
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import serializers, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny

from university.models import Motivation, Specialty, Survey, University, Faculty, UniversityPassPoint, UserPassPoint
from university.serializers import DetailedReadFacultySerializer, MotivationSerialzier, SpecialtyDetailedSerializer, SpecialtySerializer, UniversityDetailedReadSerializer, UniversityDetailedSerializer, UniversityPassPointSerializer, UniversitySerializer, FacultySerializer, DetailedFacultySerializer, UserPassPointSerializer
from university.services import count_score


class UniversityView(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    queryset = University.objects.all()

    def list(self, request):
        serializer = UniversitySerializer(self.queryset, many=True)

        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        university = self.get_object()
        serializer = UniversityDetailedReadSerializer(university)

        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def survey_save(self, request):
        data = request.data
        user = request.user
        for survey in data['surveys']:
            print(survey)
            Survey.objects.create(user=user, string=survey)
        return Response()
    
    @action(detail=False, methods=['get'])
    def survey_get(self, request):
        user = request.user
        surveys = Survey.objects.filter(user=user)
        if surveys:
            data = []
            for survey in surveys:
                data.append(survey.string)
            json = {
                "surveys":data
            }
            return Response(json)
        return Response()
    
    @action(detail=False, methods=['get'])
    def user_results_list(self, requeset):
        university = UniversityPassPoint.objects.all()
        serializer = UniversityPassPointSerializer(university, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def university_pass(self, request):
        data = request.data
        user = request.user
        university_pass = UniversityPassPoint.objects.filter(university_id=data['university'],
                                                            faculty_id=data['faculty'],
                                                            specialty_id=data['specialty']).values_list('pass_point', flat=True)
        if len(university_pass) == 0:
            return Response({"detail": "Not found such university datas"})
        percent = count_score(user, data, university_pass)

        return Response({"result": f"{int(percent)}%"})
    
    @action(detail=False, methods=['get'])
    def user_results(self, request):
        user = request.user
        user_pass = UserPassPoint.objects.filter(user_id=user.id)
        serializer = UserPassPointSerializer(user_pass, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def user_results(self, request, pk):
        try:
            user_pass = UserPassPoint.objects.get(id=pk)
            serializer = UserPassPointSerializer(user_pass)
            return Response(serializer.data)
        except:
            return Response({"detail": "Not found"})
    
    @action(detail=True, methods=['get'])
    def specialities(self, request, pk):
        try:
            uni = Faculty.objects.filter(university__id=pk)
            serializer = DetailedReadFacultySerializer(uni, many=True)
            return Response(serializer.data)
        except:
            return Response({"detail": "Not found"})
        
class FacultyView(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    queryset = Faculty.objects.all()

    def list(self, request):
        serializer = FacultySerializer(self.queryset, many=True)

        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        faculty = self.get_object()
        serializer = FacultySerializer(faculty)

        return Response(serializer.data)
    
    @action(methods=['get'], detail=True)
    def university(self, request, pk):
        faculties = Faculty.objects.filter(university=pk)
        serializer = FacultySerializer(self.queryset, many=True)

        return Response(serializer.data)        

    #TODO: Список универов При клике на обьект показывает -> Список професси каждого уника и проф предметы
    @action(methods=['GET'], detail=False)
    def f(self, request):
        faculty = Faculty.objects.all()
        serializer = DetailedFacultySerializer(faculty, many=True)
        print(serializer)
        return Response(serializer.data)

class SpecialtyView(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    queryset = Specialty.objects.all()

    def list(self, request):
        serializer = SpecialtySerializer(self.queryset, many=True)

        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        faculty = self.get_object()
        serializer = SpecialtyDetailedSerializer(faculty)

        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def faculty(self, request, pk):
        faculties = Specialty.objects.filter(faculty=pk)
        serializer = SpecialtySerializer(self.queryset, many=True)
        return Response(serializer.data)

    # def retrieve(self, request):
    #     uni_id = request.GET.get('uni_id')
    #     spec_id = request.GET.get('spec_id')
    #     university = University.objects.filter(id=uni_id).first()
    #     faculty = Faculty.objects.get(university=university)
    #     specialty = Specialty.objects.filter()
    #     serializer = SpecialtyDetailedSerializer(self.queryset, many=True)

    #     return Response(serializer.data)

class MotivationView(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    queryset = Motivation.objects.all()

    def list(self, request):
        serializer = MotivationSerialzier(self.queryset, many=True)

        return Response(serializer.data)
