from setuptools import find_packages, setup

with open("README.md") as readme_file:
    readme = readme_file.read()

requirements = [
    "numpy",
    "openai",
    "pandas",
    "torch",
    "transformers",
    "accelerate",
]

test_requirements = [
    "mypy",
    "lxml",
    "tqdm-stubs",
    "pylint",
    "pylint-json2html",
    "pylint-exit",
    "pytest",
    "pytest-html",
    "coverage",
]

setup(
    name="probsem",
    version="0.1.0",
    description="probabilistic semantic parsing via program synthesis",
    long_description=readme,
    author="Benjamin Lipkin",
    author_email="lipkinb@mit.edu",
    license="MIT",
    packages=find_packages(where="probsem"),
    install_requires=requirements,
    extras_require={"test": test_requirements},
    python_requires=">=3.10",
)
