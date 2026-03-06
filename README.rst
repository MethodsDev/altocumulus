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

   alto terra storage_estimate --html-output storage_report.html

This will create an interactive HTML report with workspace storage costs, or use ``--output`` for TSV format.

**Options:**

- ``--output OUTPUT``: Path to output TSV file
- ``--html-output HTML_OUTPUT``: Path to output HTML report
- ``--access {owner,reader,writer}``: Filter by workspace access level (can specify multiple times)

Note: At least one of ``--output`` or ``--html-output`` must be specified.

**Output Formats:**

1. **TSV format** (``--output``): Tab-separated file for data processing with columns: ``namespace``, ``name``, and ``estimate`` (monthly cost in USD)
2. **HTML format** (``--html-output``): Interactive web report with sortable tables

**HTML Report Features:**

- **Interactive bar chart** showing top 50 workspaces by cost (horizontal bars, color-coded)
- Interactive sortable table (default: sorted by cost descending)
- Color-coded costs (red >$10, orange >$1, green >$0)
- Summary statistics dashboard (total workspaces, total cost, average cost)
- Search and filter capabilities
- Pagination for large workspace lists
- Hover tooltips on chart bars showing exact costs

**Examples:**

.. code-block:: bash

   # Generate interactive HTML report
   alto terra storage_estimate --html-output report.html

   # Generate TSV data file
   alto terra storage_estimate --output costs.tsv

   # Generate both formats
   alto terra storage_estimate --output costs.tsv --html-output report.html

   # Filter by access level
   alto terra storage_estimate --html-output report.html --access reader

   # Multiple access levels
   alto terra storage_estimate --html-output report.html --access owner --access reader

**Note:** You must be authenticated with Terra/FireCloud. The command uses your existing ``gcloud`` credentials.
