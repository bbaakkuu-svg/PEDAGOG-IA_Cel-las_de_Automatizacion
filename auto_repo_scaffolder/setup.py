from setuptools import setup, find_packages

setup(
    name="auto-repo-scaffolder",
    version="0.1.0",
    author="Antigravity Célula Docensas",
    description="Automatización para la creación de repositorios bajo el estándar Reitz y Arquitectura Limpia.",
    packages=find_packages(),
    install_requires=[
        "pydantic>=2.0.0",
        "jinja2>=3.0.0",
        "rich>=10.0.0",
    ],
    entry_points={
        "console_scripts": [
            "scaffold=auto_repo_scaffolder.cli:main",
        ],
    },
    python_requires=">=3.9",
)
