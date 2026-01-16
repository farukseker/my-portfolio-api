from django.tasks import task
from analytical.snapshots import RequestSnapshot


@task
def view_count_with_rule_task(page_id: int, request_snapshot: RequestSnapshot, is_superuser: bool = False):
    from pages.models import PageModel
    from analytical.utils import ViewCountWithRule

    page = PageModel.objects.get(id=page_id)
    ViewCountWithRule(
        page=page,
        request=request_snapshot,
        hourly_cooldown=request_snapshot.is_superuser,
    )()