import logging
import os
import sys
from enum import Enum
from io import StringIO

import requests
import torch
import torch.nn as nn
import torch.optim as optim
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split

from .templates import TemplateMLP, TemplateRNN
from .utils import evaluate_model, train_model

load_dotenv()


class Language(str, Enum):
    python = 25


RAPIDAPI_KEY = os.getenv("JUDGE0_KEY")
RAPIDAPI_HOST = os.getenv("JUDGE0_HOST")

utils_file_path = "app/modules/utils.py"

activation_mapping = {
    "relu": nn.ReLU(),
}


class AutoChecker():
    def __init__(self, task: dict, attempt_text: str):
        self.params = task['solution_params']
        self.attempt_text = attempt_text
        logging.info(f"Task: {task}")

        if "activation" in task["solution_params"]:
            task["solution_params"]["activation"] = activation_mapping[task["solution_params"]["activation"]]

        if task["template_type"] == 'MLP':
            self.solution = TemplateMLP(**task['solution_params'])
        elif task["template_type"] == 'RNN':
            self.solution = TemplateRNN(**task['solution_params'])
        else:
            raise Exception('Invalid solution type')

    def generate_full_attempt(self, num_samples: int = 100) -> str:
        with open(utils_file_path, 'r') as f:
            utils = f.read()

        test_code = f"""
X_train, X_test, y_train, y_test = train_test_split(
    torch.randn({num_samples}, {self.params["input_size"]}),
    torch.randint(0, {self.params["output_size"]}, ({num_samples},)),
    test_size=0.2,
    random_state=42
)

# Define loss function and optimizer
criterion = nn.CrossEntropyLoss()  # Cross entropy loss is suitable for classification tasks
optimizer = optim.Adam(model.parameters(), lr=0.001)  # Adam optimizer

model = train_model(model, X_train, y_train, criterion, optimizer)
score = evaluate_model(model, X_test, y_test, criterion)
        """
        return utils + self.attempt_text + test_code

    def expected_output(self):
        X_train, X_test, y_train, y_test = train_test_split(
            torch.randn(100, self.params["input_size"]),
            torch.randint(0, self.params["output_size"], (100,)),
            test_size=0.2,
            random_state=42
        )
        sys.stdout = StringIO()
        train_model(self.solution, X_train, y_train, nn.CrossEntropyLoss(
        ), optim.Adam(self.solution.parameters(), lr=0.001))
        evaluate_model(self.solution, X_test, y_test, nn.CrossEntropyLoss())
        expected_output = sys.stdout.getvalue()
        sys.stdout = sys.__stdout__
        return expected_output


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
    url = "https://judge0-extra-ce.p.rapidapi.com/submissions"
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
