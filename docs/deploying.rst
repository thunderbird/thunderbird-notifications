=================
Deploying changes
=================

Deployment is handled automatically by GitHub Actions. When changes to notification
YAML files are merged into ``main``, the CI pipeline converts YAML to JSON, validates
it, and deploys to AWS via Pulumi.

Automated workflow
------------------

On every push to ``main`` that touches ``stage/yaml/``, ``prod/yaml/``, ``schema.json``,
``pulumi/``, ``src/``, or ``.github/workflows/``:

1. The **validate** job converts all YAML files to JSON and validates them against the schema.
2. The **deploy-stage** job automatically runs ``pulumi up`` for the ``stage`` stack.
3. The **deploy-prod** job waits for manual approval in the GitHub Actions UI (via the
   ``production`` environment protection rule), then runs ``pulumi up`` for the ``prod`` stack.

Pull requests run only the validate job, so broken YAML is caught before merge.

Approving a production deployment
----------------------------------

After a push to ``main``, navigate to the workflow run in GitHub Actions. The
``deploy-prod`` job will show as "Waiting for review". Click **Review deployments**,
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
