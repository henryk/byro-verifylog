import setuptools

setuptools.setup(
    name="byro-verifylog",
    version="0.0.1",
    author="Henryk Plötz",
    author_email="henryk@ploetzli.ch",
    description="Verify byro logchain",
    url="https://github.com/henryk/byro-verifylog",
    packages=setuptools.find_packages(),
    install_requires=[
        'canonicaljson==1.1.4',  # https://github.com/matrix-org/python-canonicaljson/blob/master/CHANGES.md
        'pynacl==1.3.0',  # https://github.com/pyca/pynacl/blob/master/CHANGELOG.rst
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'byro-verifylog = byro_verifylog.main:main'
        ]
    }
)
