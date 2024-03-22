# Squad-Mandalore-Backend
## Setup

1. Clone Git Project ```https://github.com/Squad-Mandalore/Backend.git``` (Make sure you've set the proxy)

2. Install requirements -> See requirements below

3. Setup completed!


## Requirements

### Installing PIP

In order to install packages in python you need PIP.

0. Check if you already have pip installed by running ```pip``` in the command line. If you do, you can skip the installing PIP step.

1. Download (right-click save as) the following script: ```https://bootstrap.pypa.io/get-pip.py```

2. Navigate to the Directory where you saved the script using cmd and run ```python .\get-pip.py```

3. Add pip to your environment variables by copying the installation path (should be printed out in your command line after successfully installing) and adding the path to your windows environment variables.

4. Open a new cmd and type in ```pip```, if you get a bunch of commands you've successfully installed pip!

### Create a Python virtual environment

In order to make sure the project's package versions are not interfering with your other projects it is recommended to set up a Python virtual environment.

1. Use cmd to navigate to the directory of this repository

2. Run ```python -m venv venv``` to create a virtual environment

3. Run ```venv\Scripts\activate``` to activate the virtual environment or ```venv\bin\activate``` to activate it on a Unix based system

4. If it says (venv) to the left of your input line in cmd you've successfully set up a virtual environment!

### Installing required packages using PIP

1. Use cmd to navigate to the directory of this repository

2. Make sure your virtual environment is active

3. Run ```pip install -r requirements.txt```

4. You've successfully installed all requirements! (To check your versions you can run ```pip list``` or ```pip freeze```)

### Setting up environment variables

Make sure you have the necessary variables set up in your environment variables (You can find the necessary variables in the Dockerfile file)

## Starting

```console
uvicorn src.main:app --log-config=log_conf.yaml
```

Additionally you can add the --reload flag to reload the application after making source code changes.

## Testing

Go to your project root and execute tests with:

```console
pytest
```

The framework recognizes test files, when they start with 'test_'.
Note that this approach does not work with in-memory databases.

## Configuration

### Secrets

Secrets are stored in the [GitHub repository secrets](https://github.com/Squad-Mandalore/Backend/settings/secrets/actions).
To add a secret to the repository, click on the "New repository secret" button and add the secret name and value.
Additionally, you have to add them on the build-args in the Docker workflow file and in the Dockerfile respectively.
