from django.utils import timezone


def current_time_ho(request):
    cureent_time = timezone.now().year
    return {"ct":cureent_time}