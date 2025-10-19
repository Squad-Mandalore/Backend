# Squad-Mandalore-Backend
## Setup

1. Clone Git Project ```https://github.com/Squad-Mandalore/Backend.git``` (Make sure you've set the proxy)

2. Install requirements -> See requirements below

3. Setup completed!

## Requirements

### Installing UV
https://docs.astral.sh/uv/getting-started/  

In order to install packages, managed development environment and starting the Application you need astral-uv.

0. Check if you already have pip installed by running ```uv``` in the command line. If you do, you can skip the installing PIP step.

1. Execute the following script: 
    a. (macOS/Linux) ```curl -LsSf https://astral.sh/uv/install.sh | sh```
    b. (Windows Powershell) ```powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"```

2. Open a new console and type in ```uv --help```, if you get a bunch of commands you've successfully installed pip!

Helpful scripts:  
- Initialize Python Project: ```uv sync```
- Activate Virtual environment
    - (macOS/Linux) ```source .venv/bin/activate```
    - (Windows) ```./.venv/Scripts/activate```
- Add (dev) Dependency ```uv add (--dev) <dependency>```
- Upgrade Dependencies ```uv lock --upgrade```

Tooling  
- Formating: ```ruff format```
- Linting(fix): ```ruff check (--fix)```
- Pytest(coverage) ```pytest --cov=. -coverage-report=show-missing```

For Local Test
- Build: ```docker build --tag backend --build-arg PEPPER=potato --build-arg KEYCHAIN_NUMBER=42 --build-arg JWT_KEY=potato .```
- Run: ```docker run -p 8000:8000 backend```

### Setting up environment variables

Make sure you have the necessary variables set up in your environment variables (You can find the necessary variables in the Dockerfile file)

## Starting

```console
uv run fastapi dev src/main.py
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
