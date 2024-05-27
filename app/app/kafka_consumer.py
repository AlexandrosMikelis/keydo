import os
import faust
import django

# eventlet is used as a bridge to communicate with asyncio
os.environ.setdefault("FAUST_LOOP", "eventlet")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

# Django logic models only imported after django setup is called

from consumer.models import Keystroke
from consumer.service import persist_userKeystrokes_event

from django.conf import settings

app = faust.App("core", broker=f"kafka://{settings.KAFKA_URL}")


topic = app.topic(settings.KAFKA_STREAM_TOPIC, value_type=Keystroke)


@app.agent(topic)
async def process_topic(stream):
    async for event in stream:
        print("received event %s", event)
        await persist_userKeystrokes_event(event)