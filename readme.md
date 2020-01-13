# Orchestrator engine

You've installed Python and the other utilities (pip, virtualenv, and git) on
your computer, right? If not, [head here to
install](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-ubuntu-18-04-quickstart).

First thing we need to do is create a folder for your project. If you'd like to do this as well, follow these
commands in your terminal to create the projects folder, and a folder within for this individual project:

```bash
$ mkdir projects
$ cd projects
```

If you need a command line review, `mkdir` creates folders, and `cd` changes
directories into that folder. If you ever get lost, your terminal should show
which directory you're in, and running `ls` (on Mac or Linux, `dir` on Windows),
will list out the contents of the folder you're in. Use `cd ..` to back up out
of a folder.

### Clone the project

Now that you're within your empty project folder, clone the project and make a copy of the `.env.example` file.

```bash
$ git clone git@github.com:marcus-campos/orchestrator-engine.git
$ cd orchestrator-engine
$ cp orchestrator/.env.example orchestrator/.env
```

### Start your virtual environment

Now, create your virtual environment.

```bash
$ virtualenv venv
```

And then activate the environment:

```bash
$ source venv/bin/activate --python=python3.8
```

You should see something like this in your command line before the folder
structure - the (venv) indicates you're in the virtual environment:

```
(venv) root@MBP ~/projects/orchestrator-engine $
```

(MBP is my computer's name and root is my username - your exact setup
will be different.)

Now you're in your bubble, so we can start installing project-specific utilities.
If you ever need to deactivate your environment, run `deactivate`.

### Install requirements

Finally, it's requirements time! We'll use `pipenv` to install requirements, so run this in your
command line, making sure you're in your project folder and the virtual
environment is activated:

```bash
$ pip install pipenv
$ pipenv install
```

We're telling pipenv to install a specific version of requirements.


## Start your Orchestrator engine

Want to see if everything worked? In your terminal, head over to your top level
orchestrator-engine folder (make sure you're in the folder with *Makefile*) and run
this command:

```
$ make runserver
```

...and you'll see the local orchestrator development server starting, which'll serve
your project to your computer.

```
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 219-974-791
```