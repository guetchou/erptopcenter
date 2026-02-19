from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read() if f.readable() else ""

setup(
    name="topcenter_finance",
    version="1.0.0",
    description="Extensions Finance / Trésorerie TopCenter (optionnel)",
    long_description=long_description or "TopCenter Finance",
    long_description_content_type="text/markdown",
    author="Top Center",
    author_email="contact@topcenter.cg",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[],
)
