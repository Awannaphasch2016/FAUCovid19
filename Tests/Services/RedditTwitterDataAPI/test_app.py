#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""test_app_response"""
import random

import pytest
from flask_api import status

from global_parameters import ALL_ASPECTS
from global_parameters import ALL_CRALWERS
from global_parameters import ALL_REDDIT_FEILDS
from global_parameters import ALL_TWITTER_FEILDS


@pytest.mark.parametrize(
    "request_value,responds_value",
    {
        (i, i) for i in ALL_CRALWERS
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

@pytest.mark.parametrize(
    "request_value,responds_value",
    [
        (i, i) for i in ALL_REDDIT_FEILDS
    ],
)
def test_fields_parameter(client,
                          request_value,
                          responds_value):
    x = client.get(f"/fields?={request_value}")
    assert status.HTTP_404_NOT_FOUND == int(x.status.split(" ")[0])

class TestAllValue:
    def test_crawler_parameters_with_all_value(self,
                                               client):
        concat_crawlers = ','.join(ALL_CRALWERS)
        x = client.get("/?crawlers=all")
        y = client.get(f"/?crawlers={concat_crawlers}")
        assert status.HTTP_200_OK == int(x.status.split(" ")[0])
        assert status.HTTP_200_OK == int(y.status.split(" ")[0])

        x = x.json["all_retrived_data"]
        y = y.json["all_retrived_data"]
        assert len(y) == len(x)

    def test_aspects_parameter_with_all_value(self,
                                              client):
        concat_crawlers = ','.join(ALL_ASPECTS)
        x = client.get("/?aspects=all")
        y = client.get(f"/?aspects={concat_crawlers}")
        assert status.HTTP_200_OK == int(x.status.split(" ")[0])
        assert status.HTTP_200_OK == int(y.status.split(" ")[0])

        assert y.json["all_retrived_data"][0]['aspect'] \
               == x.json["all_retrived_data"][0]['aspect']

    def test_fields_parameter_with_all_value(self,
                                             client):
        concat_crawlers = ','.join(ALL_ASPECTS)
        x = client.get("/?aspects=all")
        y = client.get(f"/?aspects={concat_crawlers}")
        assert status.HTTP_200_OK == int(x.status.split(" ")[0])
        assert status.HTTP_200_OK == int(y.status.split(" ")[0])
        assert y.json["all_retrived_data"][0]['aspect'] \
               == x.json["all_retrived_data"][0]['aspect']




class TestRedditParameters():


    @pytest.mark.parametrize(
        "request_value,responds_value",
        [
            (i, i) for i in ALL_REDDIT_FEILDS
        ],
    )
    def test_reddit_fields_parameter(self,
                                     client,
                                     request_value,
                                     responds_value):
        x = client.get(f"/?crawlers={ALL_CRALWERS[1]}&fields={request_value}")
        assert status.HTTP_200_OK == int(x.status.split(" ")[0])
        assert f'{responds_value}' \
               == list(x.json["all_retrived_data"][0].keys())[0]

    def test_reddit_fields_parameters_random_combination(self,
                                                         client):
        sampled_fields = random.sample(ALL_REDDIT_FEILDS, 5)
        sampled_fields = ','.join(sampled_fields)
        x = client.get(f"/?crawlers={ALL_CRALWERS[1]}&fields={sampled_fields}")
        assert status.HTTP_200_OK == int(x.status.split(" ")[0])
        assert f'{sampled_fields}' \
               == ','.join(list(x.json["all_retrived_data"][0].keys()))


class TestTwitterParamter:

    @pytest.mark.parametrize(
        "request_value,responds_value",
        [
            (i, i) for i in ALL_TWITTER_FEILDS
        ],
    )
    def test_twitter_fields_parameter(self,
                                      client,
                                      request_value,
                                      responds_value):
        x = client.get(f"/?crawlers={ALL_CRALWERS[0]}&fields={request_value}")
        assert status.HTTP_200_OK == int(x.status.split(" ")[0])
        assert f'{responds_value}' \
               == list(x.json["all_retrived_data"][0].keys())[0]

    def test_twitter_fields_parameters_random_combination(self,
                                                          client):
        sampled_fields = random.sample(ALL_TWITTER_FEILDS, 5)
        sampled_fields = ','.join(sampled_fields)
        x = client.get(f"/?crawlers={ALL_CRALWERS[0]}&fields={sampled_fields}")
        assert status.HTTP_200_OK == int(x.status.split(" ")[0])
        assert f'{sampled_fields}' \
               == ','.join(list(x.json["all_retrived_data"][0].keys()))

