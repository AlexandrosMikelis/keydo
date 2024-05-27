from asgiref.sync import sync_to_async

from core.models import UserKeystrokes


@sync_to_async
def persist_userKeystrokes_event(event):
    UserKeystrokes.objects.create(
        user=event.user,
        keystroke_id=event.keystroke_id,
        key_code=event.key_code,
        event=event.event,
        timestamp=event.timestamp,
    )