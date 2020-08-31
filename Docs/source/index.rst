.. FAUCOVID19 documentation master file, created by
    sphinx-quickstart on Sun Aug 30 11:29:22 2020.
    You can adapt this file completely to your liking, but it should at least
    contain the root `toctree` directive.

Welcome to FAUCOVID19's documentation!
*****************************************

How to use TwitterRedditAPI with Examples
==============================================

Note that parameters below can be used in combination. (this does not include 'all' value behavior)

For 'all' parameters behavior see "'all' behavior" section. This is important because 'all' value is
default for any fields that accept list of value (easy way to remember is any parameters that are in plural form accepts list of value).
unless specified otherwise
(without knowning 'all' behavoir you could encounter 'unexpected' returned value)

Users can pass in following parameters:

* 'crawlers'           = Select type of crawler to pull stored crawled date from

.. code-block::

   localhost:5000/?crawlers=all

* 'since' and 'until' = Select range of data in contained database. The accepted format of date is '%Y-%m-%d' eg. 2020-08-12

.. code-block::

   localhost:5000/?crawlers=reddit
.. code-block::

   localhost:5000/?crawlers=reddit,twitter

* 'fields'            = Select fields to be shown as output keys in json format. Reddit and Twitters have unquie fields. (this is because of twitter or reddit api that are used )

Note: fields of reddit and twitter are 'forced' to be as similar as possible

* Note: that twitter's 'date' == reddit's 'created_utc' ( I missed it and it should be changed whenever possible)

   - common fields => 'aspect', 'search_types', 'crawler', 'frequency', 'id', 'sentiment'

   - reddit's fields =>  'created_utc',  'subreddit', 'link_id', 'parent_id', 'title', 'body'

   - twitter's fields =>  'text', 'date'

without specified crawler

.. code-block::

   localhost:5000/?fields=aspect,search_type

with specified crawler. Notice that I can use fields specific to a specified crawler

.. code-block::

   localhost:5000/?crawlers=reddit&fields=aspect,search_type,subreddit

* 'search_types'       = Select search type. Each social media has different set accpeted of search_type value. This is due to nature of how each site structured their data.

    - reddit's search_type => 'comment', 'submission'
    - twitter's search_type => 'data_tweet'

.. code-block::

   localhost:5000/?crawlers=twitter&search_types=data_tweet

* 'aspects'            = Select aspects consist of 5 categories: 'work_from_home', 'reopen', 'lock_down', 'corona', and 'social_distance'

.. code-block::

   localhost:5000/?aspects=work_from_home,lock_down

* 'frequency'         = Select 'interval' types. At the moment, only frequency='day' is supported. It is used with either with 'after' or 'until'. Default value is set to 'day' because 'day' is currently the only supported frequency.

.. code-block::

   localhost:5000/?frequency=day

Example of url requests when used combination of parameters

* crawl all reddit data, but only output crawler, body, and sentiment

.. code-block::

   localhost:5000/?crawler=reddit&fields=crawler,body,sentiment

* crawl twitter data from 2020-8-20 to 2020-8-30 for aspects related to 'work_from_home'


Note: that you must specified "aspect", its 'collections', and its 'query' list by yourself.

.. code-block::

   localhost:5000/?crawler=twitter&fields=body&since=2020-8-20&until=2020-8-30&aspect=work_from_home


'all' Behavior
===============

Note: this 'all' behavior encorage users to send request each crawler separately in case that "crawler=all" behavior is not desired. (more detail below)

warning: for any fields that accept 'all' value, not passing any value is equvilent to passing "param=all" (default value is set to 'all')

Note: parameter that accepts 'all' value are the following => crawlers, fields, aspects and  search_type. Also when no value is passed for since and until, data for all date will be provided.

when user specify crawler='all' => it is equivalent to 'crawler=<all of crawler availbel>' (note that <> represents variables not actual str that will be used).
Furthermore, crawler = 'all' is a behavior that is an except to the design. Code design encorage user to request data of 1 crawler at a time.


Use Case where one may prefer sending per specified crawler

*  one may want differents fields for different crawler, one must send 2 requests with different fields.




Start Here!!
==============

.. toctree::
   :maxdepth: 4

   installation
   get_started

Crawler Documentation
========================

.. toctree::
   :maxdepth: 4

   twitter_crawler
   reddit_crawler
   social_media_crawler

TwitterRedditAPI Documentation
==================================

.. toctree::
   :maxdepth: 4

   update_sqlite3_database
   app


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


TODO
======
* allow simply list of query search in all crawler types
