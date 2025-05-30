from setuptools import setup, find_packages

setup(
    packages=find_packages(
        include=["api", "agents", "models", "clients", "context", "prompts", "resources", "data_sources", "tests", "tools", "utils"]),
)
