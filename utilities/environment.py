from dotenv import load_dotenv
import os

def load_env_dev() -> None:
    """Loads environment variables if application is being run in the development environment"""
    if os.getenv("ENVIRONMENT") == None:
        load_dotenv()

def get_env_var(name: str) -> str:
    """Retrieves an environment variable and if it does not exist, throws an `EnvironmentError`"""
    load_env_dev()
    variable = os.getenv(name)
    if not variable:
        raise EnvironmentError(f'Missing environment variable: {name}')
    return str(variable)
