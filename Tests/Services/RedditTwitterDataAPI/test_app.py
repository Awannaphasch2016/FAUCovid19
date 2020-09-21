#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""test_app_response"""
import random

import pytest
from flask_api import status

from global_parameters import ALL_ASPECTS
from global_parameters import ALL_CRALWERS
from global_parameters import ALL_FREQUENCY
from global_parameters import ALL_REDDIT_FEILDS
from global_parameters import ALL_REDDIT_SEARCH_TYPES
from global_parameters import ALL_TWITTER_FEILDS
from global_parameters import ALL_TWITTER_SEARCH_TYPES


@pytest.mark.test_parameter
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


@pytest.mark.test_parameter
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


@pytest.mark.test_parameter
@pytest.mark.parametrize(
    "request_value,responds_value",
    [
        (i, i) for i in ALL_REDDIT_FEILDS
    ],
)
def test_fields_parameter_faile(client,
                                request_value,
                                responds_value):
    x = client.get(f"/?fields={request_value}")
    assert status.HTTP_400_BAD_REQUEST == int(x.status.split(" ")[0])


@pytest.mark.test_parameter
@pytest.mark.parametrize(
    "request_value,responds_value",
    [
        (i, i) for i in set(ALL_REDDIT_SEARCH_TYPES + ALL_TWITTER_FEILDS)
    ],
)
def test_search_types_parameter_fail(client,
                                     request_value,
                                     responds_value):
    x = client.get(f"/?fields={request_value}")
    assert status.HTTP_400_BAD_REQUEST == int(x.status.split(" ")[0])


@pytest.mark.test_parameter
@pytest.mark.parametrize(
    "request_value,responds_value",
    [
        (i, i) for i in ALL_FREQUENCY
    ],
)
def test_frequency_parameter(client,
                             request_value,
                             responds_value):
    x = client.get(f"/?frequency={request_value}")
    assert status.HTTP_200_OK == int(x.status.split(" ")[0])
    assert x.json["all_retrived_data"][0]['frequency'] == f'{responds_value}'


@pytest.mark.test_paramete
def test_since_parameter(client):
    x = client.get("/?since=2020-8-20")
    assert status.HTTP_200_OK == int(x.status.split(" ")[0])


@pytest.mark.test_paramete
def test_since_parameter_faile(client):
    y = client.get("/?since=20-8-20")
    assert status.HTTP_400_BAD_REQUEST == int(y.status.split(" ")[0])


@pytest.mark.test_paramete
def test_until_parameter(client):
    x = client.get("/?until=2020-8-20")
    assert status.HTTP_200_OK == int(x.status.split(" ")[0])


@pytest.mark.test_paramete
def test_until_parameter_fail(client):
    y = client.get("/?until=20-8-20")
    assert status.HTTP_400_BAD_REQUEST == int(y.status.split(" ")[0])


@pytest.mark.test_all_value
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
        x = client.get("/?fields=all")
        y = client.get(f"/?fields={concat_crawlers}")
        assert status.HTTP_400_BAD_REQUEST == int(x.status.split(" ")[0])
        assert status.HTTP_400_BAD_REQUEST == int(y.status.split(" ")[0])


@pytest.mark.test_reddit_parameters
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

    @pytest.mark.parametrize(
        "request_value,responds_value",
        [
            (i, i) for i in ALL_REDDIT_SEARCH_TYPES
        ],
    )
    def test_reddit_search_types_parameter(self,
                                           client,
                                           request_value,
                                           responds_value):
        x = client.get(f"/?crawlers={ALL_CRALWERS[1]}&search_types"
                       f"={request_value}")
        assert status.HTTP_200_OK == int(x.status.split(" ")[0])
        assert f'{responds_value}' \
               == x.json["all_retrived_data"][0]['search_type']


@pytest.mark.test_twitter_parameters
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

    @pytest.mark.parametrize(
        "request_value,responds_value",
        [
            (i, i) for i in ALL_TWITTER_SEARCH_TYPES
        ],
    )
    def test_twitter_search_types_parameter(self,
                                            client,
                                            request_value,
                                            responds_value):
        x = client.get(f"/?crawlers={ALL_CRALWERS[0]}&search_types"
                       f"={request_value}")
        assert status.HTTP_200_OK == int(x.status.split(" ")[0])
        assert f'{responds_value}' \
               == x.json["all_retrived_data"][0]['search_type']
