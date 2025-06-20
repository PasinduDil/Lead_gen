from setuptools import setup, find_packages

# Read version from __init__.py
with open('src/leadgen/__init__.py', 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.split('=')[1].strip().strip('\'"')
            break

# Read README for long description
try:
    with open('README.md', 'r') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = 'Lead generation application with multi-step questioning process'

setup(
    name="leadgen",
    version=version,
    description="Lead generation application with multi-step questioning process",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="pasindu2035@gmail.com",
    url="",
    package_dir={"":"src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "pydantic>=2.0.0",
        "pydantic-ai>=0.1.0",
        "pyyaml>=6.0",
        "httpx>=0.24.0",
    ],
    entry_points={
        "console_scripts": [
            "leadgen=leadgen.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)