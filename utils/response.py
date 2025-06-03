#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from flask import jsonify


def flask_response(code=200, message="success", data=None):
    """标准化API响应格式"""
    if message:
        base_data = {
            "success": True if code == 200 else False,
            "msg": message,
        }
        if data:
            base_data["response"] = data
    else:
        base_data = data
    return jsonify(base_data), code
