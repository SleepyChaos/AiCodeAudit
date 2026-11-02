from loguru import logger
import os
import yaml

from models import Config

def load_yaml_as_pydantic(file_path: str, model_cls:Config) -> Config:
    with open(file_path, 'r', encoding='utf-8') as file:
        data: dict = yaml.safe_load(file)
    openai_config = data.setdefault('openai', {})
    for field, env_name in (
        ('api_key', 'OPENAI_API_KEY'),
        ('base_url', 'OPENAI_BASE_URL'),
        ('model', 'OPENAI_MODEL'),
    ):
        value = os.getenv(env_name)
        if value is not None:
            openai_config[field] = value
    return model_cls(**data)
def create_default_config(file_path):
    """创建默认配置文件"""
    default_config = {
        'openai': {
            'base_url': 'https://api.openai-proxy.org/v1',
            'api_key': '',
            'model': 'gpt-4o-mini',
            'max_per_tokens': 4096
        },
        'project': {
            "source_file_ext": [".py", ".go", ".js", ".java", ".cpp", ".php", ".aspx", ".asp", ".c", ".cs"],
            "config_file_ext": [".yaml", ".xml", ".json", ".conf", ".ini", ".toml", ".config", ".settings"],
            "exclude_dir": ['node_modules', "dist", "build", "out", "venv", ".venv", "env", "target", "vendor",
                          "bower_components",
                          ".git", ".svn", ".hg", ".idea", ".vscode", ".metadata", "nbproject", "test", "tests", "spec",
                          "specs",
                          "tmp", "temp", "cache", "logs", "docker", "containers", "k8s", "kube", ".circleci", ".github",
                          ".travis", "docs", "doc", ".secrets", ".env"],
            "exclude_max_file_size": 1
        }
    }
    with open(file_path, 'w', encoding='utf-8') as file:
        yaml.dump(default_config, file, default_flow_style=False)
    logger.info(f"已创建默认配置文件: {file_path}")


def load_or_create_config(yaml_path):
    """加载或创建配置文件"""
    if not os.path.exists(yaml_path):
        logger.info(f"配置文件未找到: {yaml_path}")
        create_default_config(yaml_path)
    config=load_yaml_as_pydantic(yaml_path, Config)
    return config

