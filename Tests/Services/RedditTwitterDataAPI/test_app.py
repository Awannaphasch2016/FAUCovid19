#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""test_app_response"""

import pytest
from flask_api import status


@pytest.mark.parametrize(
    "crawler_request_value,crawler_responds_value",
    [
        ("reddit", "reddit"),
        ("twitter", "twitter"),
    ],
)
def test_crawler_parameters(
    client, crawler_request_value, crawler_responds_value,
):
    x = client.get(f"/?crawlers={crawler_request_value}")
    assert status.HTTP_200_OK == int(x.status.split(" ")[0])
    assert (
        f"{crawler_responds_value}"
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


def test_aspects_parameter(client):
    work_from_home = client.get("/?aspects=work_from_home")
    social_distance = client.get("/?aspects=social_distance")
    lockdown = client.get("/?aspects=lockdown")
    reopen = client.get("/?aspects=reopen")
    corona = client.get("/?aspects=corona")
    pass


def test_aspects_parameter_with_all_value(client):
    pass
