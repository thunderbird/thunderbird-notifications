=================
Deploying changes
=================

Ensure you're setup by following the setup instructions available `here. <https://thunderbird.github.io/pulumi/getting-started.html>`_

Additionally you'll also need a login token from pulumi cloud. The pulumi cloud account is located in the Services 1password account. Alternatively you can log-in through pulumi cloud via ``pulumi login``.

Before running
--------------

Make sure to cd into ``pulumi`` and ensure you're not in any active virtual environment. The easiest way is to just start a new shell in the current directory (i.e. run ``bash`` or ``zsh`` depending on what you use.)

Everytime you run either ``pulumi up`` or ``pulumi preview`` pulumi will ask you which stack you want to run.

If you'd like to avoid this in the future you can run ``pulumi stack select $stack``

Previewing changes
------------------

To preview changes showing the diff of the update run the following:

.. code-block:: bash

  pulumi preview --diff

No actual changes will be pushed up, this command should be safe to run at anytime.

Deploying changes
-----------------

.. code-block:: bash

  pulumi up --diff

Verifying changes
-----------------

Once you've successfully deployed your json changes you can verify that they're live by going to:

- Stage: https://notifications-stage.thunderbird.net/2.0/notifications.json
- Prod: https://notifications.thunderbird.net/2.0/notifications.json

Clearing the production cache
------------------------------

Within our Cloudflare account under the ``thunderbird.net`` domain you'll need to run a ``Custom Purge`` under ``Caching -> Configuration`` for the hostname `notifications.thunderbird.net`. 
