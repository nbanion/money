import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="money",
    version="0.0.1",
    author="Nathan Banion",
    author_email="natebanion@gmail.com",
    description="A package to manage household finances.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)
