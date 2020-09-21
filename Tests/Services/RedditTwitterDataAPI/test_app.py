#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""test_app_response"""

import pytest
from flask_api import status

from global_parameters import ALL_ASPECTS
from global_parameters import ALL_CRALWERS
from global_parameters import ALL_REDDIT_FEILDS


@pytest.mark.parametrize(
    "request_value,responds_value",
    {
        (i,i) for i in ALL_CRALWERS
    },
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
    concat_crawlers = ','.join(ALL_CRALWERS)
    x = client.get("/?crawlers=all")
    y = client.get(f"/?crawlers={concat_crawlers}")
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
    x = client.get(f"/?aspects={request_value}")

    assert status.HTTP_200_OK == int(x.status.split(" ")[0])

    assert f'{responds_value}' \
           == x.json["all_retrived_data"][0]['aspect']

def test_aspects_parameter_with_all_value(client):
    concat_crawlers = ','.join(ALL_ASPECTS)
    x = client.get("/?aspects=all")
    y = client.get(f"/?aspects={concat_crawlers}")
    assert status.HTTP_200_OK == int(x.status.split(" ")[0])
    assert status.HTTP_200_OK == int(y.status.split(" ")[0])

    assert y.json["all_retrived_data"][0]['aspect'] \
           == x.json["all_retrived_data"][0]['aspect']


# @pytest.mark.parametrize(
#     "request_value,responds_value",
#     [
#         (i, i) for i in ALL_REDDIT_FEILDS
#     ],
# )
# def test_aspects_parameter(client, request_value, responds_value):
#     x = client.get(f"/fields?={request_value}")
#     assert status.HTTP_200_OK == int(x.status.split(" ")[0])
#     assert f'{responds_value}' \
#            == x.json["all_retrived_data"][0]['aspect']

def test_fields_parameter_with_all_value(client):
    concat_crawlers = ','.join(ALL_ASPECTS)
    x = client.get("/?aspects=all")
    y = client.get(f"/?aspects={concat_crawlers}")
    assert status.HTTP_200_OK == int(x.status.split(" ")[0])
    assert status.HTTP_200_OK == int(y.status.split(" ")[0])
    assert y.json["all_retrived_data"][0]['aspect'] \
           == x.json["all_retrived_data"][0]['aspect']
