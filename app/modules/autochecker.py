import logging
import os
from enum import Enum

import requests
from dotenv import load_dotenv

load_dotenv()


class Language(str, Enum):
    python = 92
    c = 50
    cpp = 54
    java = 91
    javascript = 93
    sql = 82
    typescript = 94


RAPIDAPI_KEY = os.getenv("JUDGE0_KEY")
RAPIDAPI_HOST = os.getenv("JUDGE0_HOST")


def make_request(url, method, headers=None, params=None, json=None):
    headers = headers or {}
    headers.update({
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    })
    response = requests.request(
        method, url, headers=headers, params=params, json=json)
    return response.json()


def submit_code(source_code: str, expected_output: str, stdin: str = "", language_id: int = Language.python):
    url = "https://judge0-ce.p.rapidapi.com/submissions"
    querystring = {"base64_encoded": "false", "wait": "true", "fields": "*"}
    payload = {
        "language_id": language_id,
        "source_code": source_code,
        "expected_output": expected_output,
        "stdin": stdin
    }
    response = make_request(url, "POST", params=querystring, json=payload)
    return response


def get_submission_details(submission_token: str):
    url = f"https://judge0-ce.p.rapidapi.com/submissions/{submission_token}"
    response = make_request(url, "GET")
    return response
