=================
Deploying changes
=================

Deployment is handled automatically by GitHub Actions. When changes to notification
YAML files are merged into ``main``, the CI pipeline converts YAML to JSON, validates
it, and deploys to AWS via Pulumi.

Stage and production directories
---------------------------------

Notification YAML files are kept in separate directories per environment:

- ``stage/yaml/`` — notifications deployed to the **stage** environment.
- ``prod/yaml/`` — notifications deployed to the **production** environment.

To deploy a notification to production, its YAML file must be present in ``prod/yaml/``.
Placing a file only in ``stage/yaml/`` will deploy it to stage but not production. This
allows you to test notifications on stage before promoting them to production by copying
the file into ``prod/yaml/``.

Automated workflow
------------------

On every push to ``main`` that touches ``stage/yaml/``, ``prod/yaml/``, ``schema.json``,
``pulumi/``, ``src/``, or ``.github/workflows/``:

1. The **validate** job converts all YAML files to JSON and validates them against the schema.
2. A single **deploy** job uses a matrix strategy to run ``pulumi up`` for both the
   ``stage`` and ``prod`` stacks in parallel. The ``prod`` leg waits for manual approval
   in the GitHub Actions UI (via the ``production`` environment protection rule).

Pull requests run only the validate job, so broken YAML is caught before merge.

Approving a production deployment
----------------------------------

After a push to ``main``, navigate to the workflow run in GitHub Actions. The
``deploy (prod)`` job will show as "Waiting for review". Click **Review deployments**,
select the ``production`` environment, and approve.

Authentication
--------------

The workflow uses OIDC (OpenID Connect) for both AWS and Pulumi Cloud.

Running Pulumi manually
-----------------------

If you need to run Pulumi locally (e.g. for debugging or previewing), make sure to
``cd`` into ``pulumi/`` and ensure you're not in any active virtual environment.

You will need a login token from Pulumi Cloud.

Previewing changes:

.. code-block:: bash

  pulumi preview --diff

Deploying changes:

.. code-block:: bash

  pulumi up --diff

Verifying changes
-----------------

Once deployed, verify that notifications are live:

- Stage: https://notifications-stage.thunderbird.net/2.0/notifications.json
- Prod: https://notifications.thunderbird.net/2.0/notifications.json

Clearing the production cache
------------------------------

Within our Cloudflare account under the ``thunderbird.net`` domain you'll need to run a
``Custom Purge`` under ``Caching -> Configuration`` for the hostname
``notifications.thunderbird.net``.
