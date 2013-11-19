from test_tool.settings import DEBUG
import logging

if DEBUG:
    logging.basicConfig(level='DEBUG')
else:
    logging.basicConfig()
logger = logging.getLogger(__name__)
