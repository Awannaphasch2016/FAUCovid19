#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""test_app_response"""

import pytest
from flask_api import status

from global_parameters import ALL_ASPECTS


@pytest.mark.parametrize(
    "request_value,responds_value",
    [
        ("reddit", "reddit"),
        ("twitter", "twitter"),
    ],
)
def test_crawler_parameters(
    client, request_value, responds_value,
):
    x = client.get(f"/?crawlers={request_value}")
    assert status.HTTP_200_OK == int(x.status.split(" ")[0])
    assert (
        f"{responds_value}"
        == x.json["all_retrived_data"][0]["crawler"]
    )


def test_crawler_parameters_with_all_value(client):
    x = client.get("/?crawlers=all")
    y = client.get("/?crawlers=twitter,reddit")
    assert status.HTTP_200_OK == int(x.status.split(" ")[0])
    assert status.HTTP_200_OK == int(y.status.split(" ")[0])

    x = x.json["all_retrived_data"]
    y = y.json["all_retrived_data"]
    assert len(y) == len(x)


@pytest.mark.parametrize(
    "request_value,responds_value",
    [
        (i, i) for i in ALL_ASPECTS
    ],
)
def test_aspects_parameter(client, request_value, responds_value):
    work_from_home = client.get("/?aspects=work_from_home")

    assert status.HTTP_200_OK == int(work_from_home.status.split(" ")[0])

    assert 'work_from_home' \
           == work_from_home.json["all_retrived_data"][0]['aspect']

def test_aspects_parameter_with_all_value(client):
    pass
