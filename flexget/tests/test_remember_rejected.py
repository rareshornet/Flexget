from __future__ import unicode_literals, division, absolute_import
from builtins import *  # noqa pylint: disable=unused-import, redefined-builtin

import pytest

from flexget.utils.tools import parse_timedelta


class RejectRememberPlugin(object):
    def on_task_filter(self, task, config):
        for entry in task.all_entries:
            if isinstance(config, str):
                entry.reject(remember_time=parse_timedelta(config))
            else:
                entry.reject(remember=True)


@pytest.mark.register_plugin(RejectRememberPlugin, 'test_remember_reject', api_ver=2, debug=True)
class TestRememberRejected(object):
    config = """
        tasks:
          test:
            mock:
              - {title: 'title 1', url: 'http://localhost/title1'}
            test_remember_reject: yes
    """

    def test_remember_rejected(self, execute_task):
        task = execute_task('test')
        assert task.find_entry('rejected', title='title 1', rejected_by='test_remember_reject')
        task = execute_task('test')
        assert task.find_entry('rejected', title='title 1', rejected_by='remember_rejected'), \
            'remember_rejected should have rejected'
