from django.db import models


class Region(models.Model):
    title = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'

class City(models.Model):
    title = models.CharField(max_length=100, null=True)
    region = models.ForeignKey('school.Region', on_delete=models.CASCADE,
                                    related_name='city_region', verbose_name='Region')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'


class School(models.Model):
    title = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=150, null=True)
    city = models.ForeignKey('school.City', on_delete=models.CASCADE,
                                    related_name='school_city', verbose_name='City')

    def __str__(self):
        return "{} - {}".format(self.title, self.city)

    class Meta:
        verbose_name = 'School'
        verbose_name_plural = 'Schools'
    

class SubjectFirst(models.Model):
    title = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.title

class SubjectSecond(models.Model):
    title = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.title