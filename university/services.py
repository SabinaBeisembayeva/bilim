from university.models import UserPassPoint


def count_score(user, data, university_pass):
        avg_point = sum(university_pass)/len(university_pass)
        percent = (data['point'] * 100)/avg_point
        if percent > 100.00:
            percent = 99
        UserPassPoint.objects.create(user=user, university_id=data['university'],
                                                            faculty_id=data['faculty'],
                                                            specialty_id=data['specialty'],
                                                            result=f"{int(percent)}%")
        
        return percent
