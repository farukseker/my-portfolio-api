# app/tasks.py
from django.core.tasks import task
from analytical.snapshots import RequestSnapshot

@task
def view_count_with_rule_task(page_id: int, request_snapshot: RequestSnapshot, is_superuser: bool = False):
    from pages.models import Page
    from analytics.services import ViewCountWithRule

    page = Page.objects.get(id=page_id)

