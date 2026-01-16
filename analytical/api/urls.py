from django.urls import path
from . import views

app_name = "analytical"

urlpatterns = [
    path('ip/<ip>', views.UserFlow.as_view(), name='user_flow'),
    path('content/<pk>', views.ContentTimeTick.as_view(), name='content_time_tick'),
    path('items', views.Items.as_view(), name='items'),
    path('page/<slug:slug>/<int:count>', views.PageAnalyticalView.as_view()),
    path('visitors/<slug:name>/', views.PageVisitorsListView.as_view()),
]+[
    # matrix
    path('matrix/<name>/years', views.PageYearlyView.as_view()),
    path('matrix/<name>/<int:year>/months', views.PageYearMonthlyView.as_view()),
    path('matrix/<name>/<int:year>/<int:month>', views.PageMonthDaysView.as_view()),
    # path('matrix/<name>/<int:year>/<int:month>/week', views.PageMonthDaysListView.as_view()),
    path('matrix/<name>/<int:year>/<int:month>/day', views.PageMonthDaysListView.as_view()),
    path('matrix/<name>/<int:year>/<int:month>/<int:day>', views.PageMonthDayView.as_view()),
]


'''

# matrix-page/years
# matrix-page/<YYYY>
# matrix-page/<YYYY>/month
# matrix-page/<YYYY>/<mm>/
# matrix-page/<YYYY>/<mm>/week/<w>
# matrix-page/<YYYY>/<mm>/day/<dd>
# matrix-page/range/start-date/end date
# path('page/', include('pages.api.urls'), name='pages')

'''
