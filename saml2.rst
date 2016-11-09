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

Under Linux, it is enough to install the correct system packages. If the
buildout has already been run, you will need to remove the ``lxml`` package and
re-run buildout.  This will allow ``lxml`` to be built with awareness of the
proper C-library bindings (and get ``dm.xmlsec.binding`` built with awareness
of the proper ``lxml``).

However, under OS X the system versions of libxml2 and libxslt are not usable.
You'll need to do extra work to get appropriate versions of the packages
installed and to get the Python installations of ``lxml``, ``PyXB`` and
``dm.xmlsec.binding`` to see them.

Ubuntu Only
===========

Install the required system packages::

    $ sudo apt-get install openssl libxml2 libxml2-dev libxslt1.1 libxslt1-dev libxmlsec1 libxmlsec1-dev

OS X Only
=========

1. Install the system level software::

    $ brew install libxml2 libxslt libxmlsec1 openssl

.. note:: Please note that with the exception of libxmlsec1 these are all keg-only.
          Make note of the installation directory (It should be /usr/local/opt/<packagename>)

2. Create a virtual environment::

    $ virtualenv saml2env
    $ cd saml2env
    $ bin/python -m pip install -U pip setuptools

3. Temporarily set your system PATH to include the installed packages' config
   binaries (**do not do this permanently**)::

    $ export BASE=/usr/local/opt  # this is the install directory from step 1 above
    $ export PATH=$BASE/libxml2/bin:$BASE/libxslt/bin:$BASE/libxmlsec1/bin:$PATH

4. pip install the Python packages required::

    $ bin/python -m pip install lxml pyxb dm.xmlsec.binding cssselect

All Systems
===========

On both systems, you'll need to run the buildout.

If the buildout has been run before
-----------------------------------

You must not use a version of ``lxml`` that has been built prior to having all
the critical C-bindings in place. If you have already run buildout you must
remove the ``lxml`` package from your egg cache so that it will be rebuilt (on
Ubuntu) or skipped (on OS X).

1. Find the location of your installed ``lxml`` package::

    $ cd /path/to/isaw.web
    $ cat bin/client1 | grep lxml
    /path/to/buildout/cache/lxml-2.3.6-py2.7-macosx-10.10-intel.egg

2. Delete the package::

    $ rm /path/to/buildout/cache/lxml-2.3.6-py2.7-macosx-10.10-intel.egg

3. Delete other artifacts to force full re-build::

    $ rm .installed.cfg 

In all cases
------------

Bootstrap the buildout::

      OS X: $ /path/to/saml2env/bin/python bootstrap.py -c buildout.cfg
    Ubuntu: $ python bootstrap.py -c buildout.cfg

Run the buildout::

    $ bin/buildout -c buildout.cfg


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

