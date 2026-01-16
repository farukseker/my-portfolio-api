from rest_framework.generics import CreateAPIView
from chatwithme.api.serializers import MeetingSerializer
from chatwithme.models import MeetingModel
from rest_framework.throttling import  AnonRateThrottle


class MeetingCreateThrottle(AnonRateThrottle):
    THROTTLE_RATES: dict = {
        'anon': '2/hour'
    }

class MeetingCreateView(CreateAPIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = [MeetingCreateThrottle]
    serializer_class = MeetingSerializer
    queryset = MeetingModel.objects.all()

