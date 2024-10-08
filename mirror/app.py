#!/usr/bin/env python
import os
import json
from .utils.helper import log, giteaSession, set_config
from .utils.gistsSource import gistsSource
from .utils.repositorySource import repositorySource


def main():
    config_json_path = os.environ.get("GITHUB_MIRROR_CONFIG")
    config = json.loads(open(config_json_path).read().strip())
    set_config(config)
    giteaSession()
    if config["gistsSource"]:
        log("Setting Up Mirror For Source Github Gists")
        gistsSource()
        log("Finished")

    if config["repositorySource"]:
        log("Setting Up Mirror For Source Github Repository")
        repositorySource()
        log("Finished")


if __name__ == "__main__":
    main()
