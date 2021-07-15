# Python API Tests

## Installation to run from a terminal

1. Download [Python 3.9](https://www.python.org/downloads/)
2. Install Python from the downloaded package.
3. Clone the project, navigate to project directory from your terminal, run:
```pip3 install -r requirements.txt```

## Running from a terminal
Set environment variable ENV value (dev or prod), for example:

Linux/Mac => export ENV=dev

Windows => set ENV=prod

Default environment is dev if variable is not set.

Then run:
```python3 -m pytest --alluredir=test_results/ tests```

## Report
To generate the report (Allure need to be installed beforehand) run ```allure serve test_results -h localhost```

More about Allure implementation for pytest is [here](https://docs.qameta.io/allure/#_pytest).

## Running inside the Docker
```docker build -t pytest_runner .```

Specify valid current folder path as src for command below

```docker run --rm --mount type=bind,src=$(pwd),target=/tests_project/ pytest_runner```

OR instead of two command above, just run

```docker-compose up --build```
