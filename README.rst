==============
Altocumulus
==============

|PyPI| |Python| |License| |Docs|

.. |PyPI| image:: https://img.shields.io/pypi/v/altocumulus.svg
   :target: https://pypi.org/project/altocumulus
.. |Python| image:: https://img.shields.io/pypi/pyversions/altocumulus
   :target: https://pypi.org/project/altocumulus
.. |License| image:: https://img.shields.io/github/license/lilab-bcb/altocumulus
   :target: https://github.com/lilab-bcb/altocumulus/blob/master/LICENSE
.. |Docs| image:: https://readthedocs.org/projects/altocumulus/badge/?version=latest
   :target: https://altocumulus.readthedocs.io

Command line utilities for running workflows on `Terra <https://app.terra.bio>`_ or `Cromwell <https://cromwell.readthedocs.io>`_ including:

- Run a Terra method, and bulk add/delete methods on Terra.
- Submit WDL workflow jobs to a sever running Cromwell, as well as check jobs' status, abort jobs, and get logs.
- Replace local file paths with remote Cloud (Google Cloud or Amazon AWS) bucket URIs, and automatically upload referenced files to Cloud buckets.
- Parse monitoring log files to determine optimal instance type and disk space.

Important tools used by Altocumulus:

- `FireCloud Swagger <https://api.firecloud.org/>`_
- `Dockstore Swagger <https://dockstore.org/api/static/swagger-ui/index.html>`_
- `FireCloud Service Selector <https://github.com/broadinstitute/fiss>`_ (FISS). In particular, `fiss/firecloud/api.py <https://github.com/broadinstitute/fiss/blob/master/firecloud/api.py>`_.

Installation
------------

Install from the MethodsDev repository:

.. code-block:: bash

   git clone https://github.com/MethodsDev/altocumulus.git
   cd altocumulus
   pip install -e .

Verify installation:

.. code-block:: bash

   alto --version

Quick Start
-----------

Get Terra Workspace Storage Estimates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Export storage cost estimates for all your Terra workspaces:

.. code-block:: bash

   alto terra storage_estimate --output storage_costs.tsv

This will create a TSV file with columns: ``namespace``, ``name``, and ``estimate`` (monthly cost in USD).

**Options:**

- ``--output OUTPUT``: Path to output TSV file (required)
- ``--access {owner,reader,writer}``: Filter by workspace access level (can specify multiple times)

**Examples:**

.. code-block:: bash

   # Get estimates for all workspaces (default: owner access)
   alto terra storage_estimate --output my_costs.tsv

   # Get estimates only for workspaces where you're a reader
   alto terra storage_estimate --output reader_costs.tsv --access reader

   # Get estimates for multiple access levels
   alto terra storage_estimate --output all_costs.tsv --access owner --access reader

**Note:** You must be authenticated with Terra/FireCloud. The command uses your existing ``gcloud`` credentials.

