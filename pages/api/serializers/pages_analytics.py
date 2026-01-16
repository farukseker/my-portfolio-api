from dateutil.relativedelta import relativedelta

from rest_framework import serializers
from pages.models import PageModel
from analytical.models import ViewModel

import datetime
from django.utils import timezone
from datetime import timedelta, date
from calendar import monthrange


class ViewListAnalyticSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewModel
        fields = '__all__'


class PagesAnalyticsSerializer(serializers.ModelSerializer):
    view = ViewListAnalyticSerializer(many=True)
    hourly_plot = serializers.SerializerMethodField()
    monthly_plot = serializers.SerializerMethodField()

    def get_hourly_plot(self, instance):
        today = datetime.datetime.today()
        views = instance.view.all().filter(visit_time__day=today.day).order_by('visit_time')
        return {hour: views.filter(visit_time__hour=hour).count() for hour in range(24)}
        # return [views.filter(visit_time__hour=hour).count() for hour in range(24)]

    @staticmethod
    def generate_month_year_list(start_date, end_date):
        current_date = start_date
        result_list = []

        while current_date <= end_date:
            result_list.append((current_date.year, current_date.month))
            current_date += relativedelta(months=1)

        return result_list

    def get_monthly_plot(self, instance):

        """
        The duty of the service is to chronologically
        order the incoming view list and count month by month and year by year since the start date.
        :param instance:
        :return: {2023:{1:250,2:0}}
        :return: {YYYY:{MM:VIEW,MM+1:VIEW}}
        """

        try:
            first_visit_date = instance.view.all().order_by('visit_time').first()
            today = datetime.datetime.today() + datetime.timedelta(days=30)   # Convert today to datetime.date
            context = {}
            for year, month in self.generate_month_year_list(first_visit_date.visit_time.date(), today.date())[::-1]:
                first_day_of_month = datetime.datetime(year, month, 1).date()  # Convert to datetime.date
                last_day_of_month = first_day_of_month.replace(day=1) + relativedelta(months=1, days=-1)
                # last_day_holder = monthrange(today.year, today.month)[1]
                # last_day_of_month = datetime.date(today.year, today.month, last_day_holder)
                views = instance.view.all().filter(visit_time__range=[first_day_of_month, last_day_of_month])
                date_list = [first_day_of_month + timedelta(days=i) for i in
                             range((last_day_of_month - first_day_of_month).days + 1)]
                result = {date.day: views.filter(visit_time__day=date.day).count() for date in date_list}
                result = result.values()
                # context.append({year: {month: result}})
                if year not in context:
                    context[year] = {}
                context[year][month] = result
            # context = sorted(context, key=lambda x: (list(x.keys())[0], list(x.values())[0].keys()), reverse=True)
            return context
        except:
            pass
        finally:
            del first_visit_date
            del today
            del context

    class Meta:
        model = PageModel
        fields = ('name', 'view', 'hourly_plot', 'monthly_plot', 'image', 'title')


class PageAnalyticSerializer(serializers.Serializer):
    ...
