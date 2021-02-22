#

import sys

sys.path.insert(1, '.')
from application import get_operating_system


def test_get_operating_system():
    assert get_operating_system() == 'Windows'


def test_get_operating_system_linux(mocker):
    mocker.patch('application.is_windows', return_value=False)

    assert get_operating_system() == 'Linux'
