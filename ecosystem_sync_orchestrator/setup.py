from setuptools import setup, find_packages

setup(
    name="ecosystem-sync-orchestrator",
    version="0.1.0",
    author="Antigravity Célula Docensas",
    description="Orquestador multi-estrategia para la sincronización de activos de automatización.",
    packages=find_packages(),
    install_requires=[
        "rich>=10.0.0",
    ],
    python_requires=">=3.9",
)
