from django.db.models.signals import post_save
from django.dispatch import receiver
from chatwithme.models import MeetingModel, ChatRoom, ChatLog
from config.settings.base import CUSTOM_LOGGER


@receiver(post_save, sender=MeetingModel)
def when_organize_new_meeting_send_notification_to_admin(sender, instance, created, **kwargs):
    if created:
        CUSTOM_LOGGER.construct(
            title="Created New Meeting",
            description= instance.notes if instance.notes else "success",
            level="success",
            metadata={
                "Metrics": {
                    'title': instance.title,
                    'notes': instance.notes,
                    'email': instance.email,
                    'date': str(instance.date),
                    'meeting_id': instance.meeting_id.hex,
                },
            },
        )
        CUSTOM_LOGGER.send()

@receiver(post_save, sender=ChatRoom)
def when_start_new_chat_send_notification_to_admin(sender, instance, created, **kwargs):
    if created:
        ChatLog.objects.create(
            room=instance,
            type='ai',
            message='Selam ben Echo: '
                    'Size faruk şeker hakkında bilgi vermek için buradayım size nasıl yardımcı olabilirim?'
        )
        ...
        # CUSTOM_LOGGER.construct(
        #     title="Created New Chat Room",
        #     description= f"Created New Chat Room | {str(instance.session_id)}",
        #     level="success",
        # )
        # CUSTOM_LOGGER.send()
