import base64
import os
import requests
import sys
from st2common.runners.base_action import Action

from lib.xrmcontroller import XRMBaseAction

__all__ = [
    'RunCmd'
]


class RunFailback(XRMBaseAction):

    def run(self, address, plan_name):
        req = self.session.get(address+plan_name)
        print("status", req.status_code)
        print(req.text)

        if req.status_code == 200:
            return True
        else:
            sys.exit(1)
            return False