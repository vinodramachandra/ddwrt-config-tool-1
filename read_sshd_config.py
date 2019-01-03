#!./venv/bin/python3

import json
from lease import Lease


def readSshdSettings(sshdSettingsFile):
    with open(sshdSettingsFile) as f:
        sshdFileJson = json.load(f)

    sshd_settings = sshdFileJson['sshd_configuration']

    return sshd_settings
