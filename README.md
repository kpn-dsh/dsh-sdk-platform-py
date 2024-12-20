> [!WARNING]
> This SDK is experimental and under development

> [!TIP]
> This repository uses the excellent and _blazingly fast_ [UV](https://github.com/astral-sh/uv) as Python package manager in combination with [direnv](https://github.com/direnv/direnv) to create a fast and great development experience. You're advised to follow the steps below to get the most out of [direnv](https://github.com/direnv/direnv)

## setting up direnv

1. install Direnv on your machine, see [documentation](https://direnv.net/)

2. Create a `layout_uv` function
   we can create a direnv function that will create an UV project for us and automatically activate
   our Python virtual environment for us for amazing DX:

   ```bash
   mkdir -p ~/.config/direnv/
   touch ~/.config/direnv/direnvrc
   ```

   Configure `direnvrc` with the following lines:

   ```bash
   layout_uv() {
    if [[ -d ".venv" ]]; then
        VIRTUAL_ENV="$(pwd)/.venv"
    fi

    if [[ -z $VIRTUAL_ENV || ! -d $VIRTUAL_ENV ]]; then
        log_status "No uv project exists. Executing \`uv init\` to create one."
        uv init --no-readme
        rm hello.py
        uv venv
        VIRTUAL_ENV="$(pwd)/.venv"
    fi

    PATH_add "$VIRTUAL_ENV/bin"
    export UV_ACTIVE=1  # or VENV_ACTIVE=1
    export VIRTUAL_ENV
   }
   ```

3. Setup your python project

```bash
git clone https://github.com/kpn-dsh/dsh-sdk-platform-py.git
```

since our `.envrc` contains the line `layout uv` direnv activates the function we have declared in
the previous step and sets up a UV project accordingly

## create and upload docker images to DSH

The docker image provided has full UV support integrated, dependencies are automatically loaded from `pyproject.toml` and `uv.lock`
by default the docker points at the `main.py` file in the `src/` directory as main entrypoint for the image, feel free to change this as seen fit

## creating a docker image from the repository

1. make sure you are logged into the docker credentials that are retrieved from the DSH Harbor container registry, details about logging in and retrieving credentials can be found in the official DSH docs

2. adjust the contant vars in the `justfile` to match the environment you want to deploy the image in

3. run `just all` while in the root directory of the project. the variables defined in the previous steps will be injected into the docker image built and it will be pushed to the DSH Harbor repo

## inspect your docker image

use either the `just run` or `just dive` commands that are defined in the justfile to inspect image layers or run the image locally.
`just dive` uses the "dive" cli tool, make sure this is installed locally on your machine: [Dive github repo]https://github.com/wagoodman/dive/blob/main/README.md
