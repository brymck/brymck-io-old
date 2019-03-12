from base64 import encodebytes
from functools import lru_cache
import json
from logging import INFO, basicConfig, getLogger
import os
from pathlib import Path
from typing import Dict, Set

from dotenv import load_dotenv
from kubernetes.client import CoreV1Api, V1Secret, V1ObjectMeta
from kubernetes.config import load_kube_config

basicConfig(level=INFO, format='%(message)s')
logger = getLogger(__name__)
this_directory = Path(os.path.dirname(os.path.abspath(__file__)))


def base64encode(input_string: str) -> str:
    base64bytes = encodebytes(bytes(input_string, 'utf-8'))
    return base64bytes.decode('utf-8').rstrip("\n")


def read_environment_variable(name: str) -> str:
    try:
        return os.environ[name]
    except KeyError as e:
        logger.error(f"Missing environment variable: ${name}")
        raise e


def encode_environment_variable(name: str) -> str:
    value = read_environment_variable(name)
    return base64encode(value)


def encode_json_file_from_environment_variable(name: str) -> Dict[str, str]:
    path = Path(read_environment_variable(name))
    if not path.exists():
        raise FileNotFoundError(f"Environment variable ${name} exists but no file was found at {path}")
    file_dict = json.loads(path.read_text())
    return {k: base64encode(v) for k, v in file_dict.items()}


def source_dotenv():
    env_path = this_directory.joinpath('..', '.env')
    if env_path.exists():
        logger.info(f"Sourcing environment variables from {env_path}...")
        load_dotenv(dotenv_path=env_path)
    env_local_path = this_directory.joinpath('..', '.env.local')
    if env_local_path.exists():
        logger.info(f"Sourcing environment variables from {env_local_path}...")
        load_dotenv(dotenv_path=env_local_path)


def get_kubernetes_api() -> CoreV1Api:
    logger.info('Loading Kubernetes configuration...')
    load_kube_config()
    return CoreV1Api()


@lru_cache()
def list_secret_names(v1: CoreV1Api) -> Set[str]:
    secret_list = v1.list_namespaced_secret(namespace='default')
    return set([item.metadata.name for item in secret_list.items])


def create_secret(v1: CoreV1Api, name: str, data: Dict[str, str], typ: str = 'from-literal'):
    if name in list_secret_names(v1):
        logger.info(f"Secret {name} already exists. Skipping.")
        return

    logger.info(f"Creating {name}...")
    metadata = V1ObjectMeta(name=name, namespace='default')
    secret = V1Secret(api_version='v1', kind='Secret', metadata=metadata, type=typ, data=data)
    return v1.create_namespaced_secret(namespace='default', body=secret)


def create_auth_secret(v1: CoreV1Api):
    create_secret(v1, 'auth-secret', {
        'auth_flask_secret_key': encode_environment_variable('AUTH_FLASK_SECRET_KEY'),
        'auth0_client_id': encode_environment_variable('AUTH0_CLIENT_ID'),
        'auth0_client_secret': encode_environment_variable('AUTH0_CLIENT_SECRET'),
    })


def create_kaniko_secret(v1: CoreV1Api):
    create_secret(v1, 'kaniko-secret', encode_json_file_from_environment_variable('KANIKO_SECRET'))


def main():
    source_dotenv()
    v1 = get_kubernetes_api()
    create_auth_secret(v1)
    # create_kaniko_secret(v1)


if __name__ == "__main__":
    main()
