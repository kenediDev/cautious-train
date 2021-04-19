import logging
import json

logger = logging.getLogger(__name__)

with open("core/setup_test/requirements.json", 'r') as r:
    readme = json.loads(r.read())
