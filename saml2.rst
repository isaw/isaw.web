******************************
Setup for saml2 authentication
******************************

To use the `collective.saml2 <https://github.com/collective/collective.saml2>`_
PAS plugin, a few things must be in place first.

**OS Packages:**

* libxml2
* libxslt
* libxmlsec1
* openssl

**Python Packages:**

* lxml
* dm.xmlsec.binding
* PyXB

In order to get this set up, we'll use a virtual environment.

In Development
==============

Follow these instructions to get the OS packages installed and set up the
virtual environment in development:

1. Install the system level software, if it is not already installed:

on OS X::

    $ brew install libxml2 libxslt libxmlsec1 openssl

.. note:: Please note that with the exception of libxmlsec1 these are all keg-only.
          Make note of the installation directory (It should be /usr/local/opt/<packagename>)



2. Create a virtual environment

on OS X::

    $ virtualenv saml2env
    $ cd saml2env
    $ bin/python -m pip install -U pip setuptools

3. Set your system PATH to include the installed packages' config binaries::

    $ export BASE=/usr/local/opt  # this is the install directory from step 1 above
    $ export PATH=$BASE/libxml2/bin:$BASE/libxslt/bin:$BASE/libxmlsec1/bin:$PATH

4. pip install the Python packages required::

    $ bin/python -m pip install lxml pyxb dm.xmlsec.binding

5. Run buildout using the virtualenv Python executable::

    $ cd ../
    $ saml2env/bin/python bootstrap.py
    ...
    $ bin/buildout

Troubleshooting
===============

Once you've installed everything as directed, you should be able to test the
installation of dm.xmlsec.binding. Start by firing up the ``zopepy`` interpreter::

    $ bin/zopepy

Next, attempt to import and initialize the ``dm.xmlsec.binding`` package:

.. code-block:: pycon

    >>> import dm.xmlsec.binding as xmlsec
    >>> xmlsec.initialize()

If you receive an error regarding missing Symbols from lxml.etree, then there
is a problem with how lxml was built. It does not have access to the
appropriate headers from the C libraries beneath it.  Uninstall it and try
again, ensuring that the paths to ``xml2-config``, ``xslt-config``, and
``xmlsec1-config`` are accessible (and found) when you install ``lxml``.

