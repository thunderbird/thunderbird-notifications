=================
Deploying Changes
=================

Ensure you're setup by following the setup instructions available `here. <https://thunderbird.github.io/pulumi/getting-started.html>`_

Additionally you'll also need a login token from pulumi cloud. The pulumi cloud account is located in the Services 1password account.

Before Running
--------------

Make sure to cd into ``pulumi`` and install the requirements.txt file via ``pip install -r requirements.txt``.

Everytime you run either ``pulumi up`` or `pulumi preview`` pulumi will ask you which stack you want to run.

Previewing Changes
------------------

To preview changes showing the diff of the update run the following:

.. code-block:: bash

  pulumu preview --diff

No actual changes will be pushed up, this command should be safe to run at anytime.

Deploying Changes
-----------------

.. code-block:: bash

  pulumu up --diff

Verifying Changes
-----------------

Once you've successfully deployed your json changes you can verify that they're live by going to:

- Stage: https://notifications-stage.thunderbird.net/2.0/notifications.json
- Prod: https://notifications.thunderbird.net/2.0/notifications.json