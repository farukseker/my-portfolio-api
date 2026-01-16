from rest_framework.generics import RetrieveUpdateDestroyAPIView
from chatwithme.api.serializers import MeetingSerializer
from chatwithme.models import MeetingModel
from rest_framework.throttling import  AnonRateThrottle


class MeetingThrottle(AnonRateThrottle):
    THROTTLE_RATES: dict = {
        'anon': '5/minute'
    }


class MeetingRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = [
        MeetingThrottle
    ]
    serializer_class = MeetingSerializer
    queryset = MeetingModel.objects.all()
    lookup_field = 'meeting_id'


