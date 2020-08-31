.. FAUCOVID19 documentation master file, created by
   sphinx-quickstart on Sun Aug 30 11:29:22 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to FAUCOVID19's documentation!
*****************************************

Examples
==========

crawl all data

.. code-block::

   localhost:5000/?crawlers=all

crawl all reddit data, but only output crawler, body, and sentiment

.. code-block::

   localhost:5000/?crawler=reddit&fields=crawler,body,sentiment

crawl twitter data from 2020-8-20 to 2020-8-30 for aspects related to 'work_from_home'


Note: that you must specified "aspect", its 'collections', and its 'query' list by yourself.

.. code-block::

   localhost:5000/?crawler=twitter&fields=body&since=2020-8-20&until=2020-8-30&aspect=work_from_home


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
