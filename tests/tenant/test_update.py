# -*- coding: utf-8 -*-

import unittest.mock

import pytest

import pycamunda.base
import pycamunda.tenant
from tests.mock import raise_requests_exception_mock, not_ok_response_mock


def test_update_params(engine_url, update_input, update_output):
    update = pycamunda.tenant.Update(url=engine_url, **update_input)

    assert update.url == engine_url + '/tenant/' + update_input['id_']
    assert update.query_parameters() == {}
    assert update.body_parameters() == update_output


@unittest.mock.patch('requests.Session.request')
def test_update_calls_requests(mock, engine_url, update_input):
    update = pycamunda.tenant.Update(url=engine_url, **update_input)
    update()

    assert mock.called
    assert mock.call_args[1]['method'].upper() == 'PUT'


@unittest.mock.patch('requests.Session.request', raise_requests_exception_mock)
def test_update_raises_pycamunda_exception(engine_url, update_input):
    update = pycamunda.tenant.Update(url=engine_url, **update_input)

    with pytest.raises(pycamunda.PyCamundaException):
        update()


@unittest.mock.patch('requests.Session.request', not_ok_response_mock)
@unittest.mock.patch('pycamunda.base._raise_for_status')
def test_update_raises_for_status(mock, engine_url, update_input):
    update = pycamunda.tenant.Update(url=engine_url, **update_input)
    update()

    assert mock.called


@unittest.mock.patch('requests.Session.request', unittest.mock.MagicMock())
def test_update_returns_none(engine_url, update_input):
    update = pycamunda.tenant.Update(url=engine_url, **update_input)
    result = update()

    assert result is None
