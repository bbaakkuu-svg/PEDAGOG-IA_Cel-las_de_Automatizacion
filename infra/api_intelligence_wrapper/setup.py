from setuptools import setup, find_packages

setup(
    name="api-intelligence-wrapper",
    version="0.1.0",
    author="Antigravity Célula Pedagog-ia",
    description="Facade Pattern para simplificar integraciones de APIs complejas.",
    packages=find_packages(),
    install_requires=[
        "pydantic>=2.0.0",
        "requests>=2.25.0",
        "rich>=10.0.0",
    ],
    python_requires=">=3.9",
)
