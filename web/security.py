# -*- coding:utf-8 -*-

import secrets
SECRET_KEY = secrets.token_urlsafe(16)

CSRF_ENABLED = True # Enable protection CSRF
CSRF_SESSION_KEY = secrets.token_urlsafe(16)


"""
Application threads. A common general assuption is
using 2 per available processor cores - to handle
imcoming requests using one and preforming background
operations using the other
"""
THREADS_PER_PAGE = 2


# Upload file max length Limit 64MB
MAX_CONTENT_LENGTH = 64 * 1024 * 1024
