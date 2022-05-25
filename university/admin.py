from django.contrib import admin
from university.models import GrantPoint, Motivation, Survey, University, Faculty, Specialty, Stuff, UniversityPassPoint, UserPassPoint


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'address', 'image')
    search_fields = ('title',)


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('title', 'faculty')
    search_fields = ('title',)

@admin.register(GrantPoint)
class GrantPointAdmin(admin.ModelAdmin):
    list_display = ('subject_first', 'subject_second', 'point', 'specialty')
    search_fields = ('specialty',)

@admin.register(Stuff)
class StuffAdmin(admin.ModelAdmin):
    list_display = ('bio', 'university', 'faculty')
    search_fields = ('university',)

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('user', 'string')
    search_fields = ('user',)

@admin.register(UniversityPassPoint)
class UniversityPassPointAdmin(admin.ModelAdmin):
    list_dislay = ('university', 'faculty', 'specialty', 'pass_point')
    search_fields = ('specialty',)

@admin.register(Motivation)
class MotivationAdmin(admin.ModelAdmin):
    list_display = ('quote',)
    search_fields = ('quote',)

@admin.register(UserPassPoint)
class UserPassPointAdmin(admin.ModelAdmin):
    list_display = ('user', 'university', 'result')
    search_fields = ('result',)
    