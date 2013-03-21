# -*- coding: utf-8 -*

from setuptools import setup

setup(
    name="scoped",
    version="0.1.0",
    packages=["scoped", "scoped.tests"],
    install_requires=[
        "Django>=1.5",
    ],
    author="Viktor Kotseruba",
    author_email="barbuzaster@gmail.com",
    description="easily add scopes to django models",
    license="MIT",
    keywords="django",
    zip_safe=True
)
