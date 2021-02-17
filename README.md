For more detail please see documentation.
=================================================

Please navigate to Docs/build/html/index.html and open it in your prefered browsered

DATABASE

reddit DATABASE workflow
    reddit 
        crawl ->
        save to Output/path ->
        udpate sqlite3 from Output/path -> 
        pull data from sqlite3 and push to api
    reddit_stream
        crawl and save to sqlite reddit/path under table = reddit_stream  ->
        modifty data in reddit_stream to reddit -> 
        pull data from sqlite3 and push to api
        
        