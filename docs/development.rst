Contributing
============

Install development dependencies in a virtual environment:

.. code-block:: bash

   python -m pip install -e '.[test]'
   python -m pytest -m 'not plotting'
   ruff check jutuldarcy tests examples docs/conf.py

Tests run small Julia simulations and compare an adjoint gradient with finite
differences. Plotting tests are opt-in: install CairoMakie, set
``PYJUTULDARCY_TEST_PLOTTING=1`` and run ``python -m pytest -m plotting``.

Documentation
-------------

Documentation uses `Sphinx <https://www.sphinx-doc.org/>`_, the
`Furo theme <https://pradyunsg.me/furo/>`_ and
`AutoAPI <https://sphinx-autoapi.readthedocs.io/>`_. Use Python 3.11 or newer for
documentation builds:

.. code-block:: bash

   python -m pip install -e '.[docs]'
   python -m sphinx -W --keep-going -b html docs docs/_build/html

Open ``docs/_build/html/index.html`` to preview the site. Warnings fail the build.
AutoAPI reads Python signatures and docstrings without importing the wrapper, so
building documentation does not install or initialize Julia. Keep wrapper-specific
behavior in these guides and link to the Julia documentation for simulator details.

The documentation workflow builds pull requests and pushes. Successful pushes to
``main`` deploy the HTML artifact to GitHub Pages using the ``github-pages``
environment. In the repository's **Settings → Pages**, select **GitHub Actions**
as the publishing source. Deployment permissions are limited to the deploy job;
pull requests build the documentation without publishing it.
