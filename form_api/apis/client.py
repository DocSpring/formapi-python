# coding: utf-8

"""
    API V1

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: v1

    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import sys
import os
import re
import time

from .pdf_api import PDFApi
from ..models import InlineResponse201Submission

class PollTimeoutError(Exception):
    pass

class Client(PDFApi):
    """
      FormAPI API Client
    """

    def generate_pdf(self, data, **kwargs):
        """
        Generates a new PDF and waits for PDF to be ready.
        :param Data data:
        :return: InlineResponse201
        """
        template_id = data.get('template_id')
        del data['template_id']

        kwargs['data'] = data
        kwargs['_return_http_data_only'] = True

        (data) = self.generate_pdf_with_http_info(template_id, **kwargs)

        submission = self.get_submission(data.submission.id)

        start_time = time.time()
        timeout = 60
        if 'timeout' in kwargs and kwargs['timeout'] is not None:
            timeout = kwargs['timeout']

        # Wait for submission to be ready
        while (submission.state != 'processed'):
            time.sleep(1)
            submission = self.get_submission(submission.id)

            if time.time() - start_time > timeout:
                raise PollTimeoutError("PDF was not ready after %d seconds!" % timeout)

        return submission