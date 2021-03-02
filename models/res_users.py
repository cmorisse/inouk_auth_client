import io
import base64
import sys
import traceback
import os
from base64 import b32encode, b64encode
from os import remove, urandom
from tempfile import mkstemp
from logging import getLogger
from contextlib import suppress

from odoo import api, fields, models, _
from odoo.exceptions import AccessError
from odoo.http import request

import requests
from requests_hawk import HawkAuth

#from ..exceptions import MissingOtpError, InvalidOtpError

_logger = getLogger(__name__)

INOUK_AUTH_SERVER = os.environ.get('INOUK_AUTH_SERVER')
INOUK_AUTH_SERVER_HAWK_ID = os.environ.get('INOUK_AUTH_SERVER_HAWK_ID')
INOUK_AUTH_SERVER_HAWK_SECRET = os.environ.get('INOUK_AUTH_SERVER_HAWK_SECRET')
INOUK_AUTH_TIMEOUT = int(os.environ.get('INOUK_AUTH_TIMEOUT', '0'))
INOUK_RESOURCE_KEY = os.environ.get('INOUK_RESOURCE_KEY')


class ISAResUsers(models.Model):
    _inherit = "res.users"

    def _check_credentials(self, password):
        """ Overload Odoo core method to add support for Inouk Auth (I Silky A)
        ISA activates only when password starts with trigger default='@@'

        :raises: AccessDenied
        :returns: -
        """
        if password.startswith('@@'):
            hawk_auth = HawkAuth(
                id=INOUK_AUTH_SERVER_HAWK_ID, 
                key=INOUK_AUTH_SERVER_HAWK_SECRET
            )
            headers = {
                "content-type": "application/json"
            } 
            payload = {
                "ressource_key": INOUK_RESOURCE_KEY,
                "request_username": self.login,
                "request_ip": request.httprequest.environ.get('HTTP_X_REAL_IP'),
                "request_http_user_agent": request.httprequest.environ.get('HTTP_USER_AGENT'),
                "request_hint": password
            }
            try: 
                resp = requests.post(
                    "https://%s/inouk_auth/login" % INOUK_AUTH_SERVER, 
                    headers=headers,
                    json=payload,
                    auth=hawk_auth,
                    timeout=INOUK_AUTH_TIMEOUT
                )
                if resp.status_code == 200:
                    if resp.json()['decision'] == 'accepted':
                        return
            except:
                exception_values = sys.exc_info()
                _logger.error("\n".join(traceback.format_exception(*exception_values)))          
        super()._check_credentials(password)

