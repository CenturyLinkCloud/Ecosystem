
Some long-running script and Blueprint operations exceed the maximum time limits applied to all CenturyLink Cloud tasks.

To successfully execute these long running jobs we can use the **Asynchronous Deploy** strategy.  In short the process
consists of these phases:

* Phase 0 - Obtain deploying customer's email address as part of the Package so we can communicate throughout the deploy
* Phase 1 - Synchronous prep - bootstrap and required services then fork off a second script that will run after the Blueprint terminates
* Phase 2 - Asynchronous step - the Blueprint is marked as completed but this script is still running.  Place any long-running activies in this script

See example scripts in this directory to use for templates.

You will need to make the following modifications:

* Update the `bpmailer.json` file and add your own SMTP relay
* Modify the package manifest UUID, name, and description.  Add any additional parameters you may need besides the email address.  This defines Phase 0.
* `install.sh` aligns with Phase 1.
* `install_phase2.sh` aligns with Phase 2.  This is where long running code should reside

