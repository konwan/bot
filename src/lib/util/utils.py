# !/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import random
import string
import uuid


def random_id(size=8):
    chars=string.ascii_uppercase + string.digits +string.ascii_lowercase
    return ''.join(random.choice(chars) for _ in range(size))
    return uuid.uuid4()
