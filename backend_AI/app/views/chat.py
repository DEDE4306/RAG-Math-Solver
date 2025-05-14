#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

from flask import Blueprint, request, current_app, send_from_directory, url_for

from config import PORT
from ..models.db import db
from ..models.model import User
from ..utils.auth import generate_token, token_required, verify_token, get_user_id, PhoneCode, LoginToken
from ..utils.response import flask_response

# chat = Blueprint('chat', __name__, url_prefix='/api/chat')
