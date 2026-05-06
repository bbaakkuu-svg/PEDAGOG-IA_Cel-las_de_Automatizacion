from setuptools import setup, find_packages

setup(
    name="cloud-native-task-scheduler",
    version="0.1.0",
    author="Antigravity Célula Pedagog-ia",
    description="Scheduler con Inyección de Dependencias para ejecución agnóstica a la nube.",
    packages=find_packages(),
    install_requires=[
        "rich>=10.0.0",
    ],
    python_requires=">=3.9",
)
