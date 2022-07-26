#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import logging
import traceback
from datetime import datetime
from config import project_path
logging.basicConfig(filename=f'{project_path}dtp.log', level=logging.INFO)


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'goods_gazer_service.settings')
    try:
        logging.info(f'Running scraping at: {datetime.now().strftime("%b %d %Y, %H:%M:%S")}')
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        logging.error(traceback.format_exc())
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
