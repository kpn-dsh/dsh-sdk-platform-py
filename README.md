# NOTE: EXPERIMENTAL

this sdk makes use of Nix in combination with direnv to allow for automatic venv creation and loading with the Python packaging tool Poetry.

# how to use

1. install Nix and enable flakes
   [nix docs]https://nixos.org/download

2. install Direnv
   [direnv docs]https://direnv.net/

3. clone this repo onto your machine

4. run `make project` in the cloned repository
   this will interactively create a poetry project for you, resulting in a poetry.lock and pyproject.toml
   `make project` will also allow direnv to load the Nix flake in your directory, this will automatically load the python venv
   inspect the makefile to see what other actions are

5. your python environment is fully loaded

# create and upload docker images to DSH

The docker image provided has full poetry support integrated, dependencies are automatically loaded from `pyproject.toml` and `poetry.nix`

by default the docker points at the `main.py` file in the `src/` directory as main entrypoint for the image, feel free to change this as seen fit

## creating a docker image from the repository

1. make sure you are logged into the docker credentials that are retrieved from the DSH Harbor container registry, details about logging in and retrieving credentials can be found in the official DSH docs

2. adjust the contant vars in the `Makefile` to match the environment you want to deploy the image in

3. run `make all` while in the root directory of the project. the variables defined in the previous steps will be injected into the docker image built and it will be pushed to the DSH Harbor repo

## inspect your docker image

use either the `make run` or `make dive` commands that are defined in the Makefile to inspect image layers or run the image locally.
`make dive` uses the "dive" cli tool, make sure this is installed locally on your machine: [Dive github repo]https://github.com/wagoodman/dive/blob/main/README.md
