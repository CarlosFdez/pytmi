The docs are created using sphinx. Make sure to install sphinx:

    pip install sphinx
    pip install sphinxcontrib-asyncio

If you get an error involving _NamespacePath, then update setuptools:

    pip install --upgrade setuptools

And then build the files by using `make html`