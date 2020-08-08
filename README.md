# ChroSePysipder
Use Chrome+Selenium in Pyspider; Reuse a Chrome window; An example to crawl Google Patent

### What is this？
1. This code is to use Chrome and Selenium in Pysipder(http://docs.pyspider.org/en/latest/) as javascript fetcher instead of its original fetcher PhantomJS. The code is based on https://www.jianshu.com/p/8d955deac99b
2. Start a new Chrome window and then re-use this window in other program.
3. A example to crawl Google Patent using Chrome+Selenium+Pyspider.

### Why use this?
1. Chrome+Selenium may be more versatile than PhantomJS which is not updated.
2. Start a new Chrome window and then login any website mannully. After that, we re-use this window to crawl website meaning we do not need to worry about the login anymore. We can also interact with this window anytime. The re-using of window also have a disadvantage, we can only crawl websites one by one meaning the speed is low.

### How to use?
1. Make sure that the Chrome webdrive, Selenium, Pyspider and Flask are corrected installed. (I use Anaconda Python 2.7 in Win10)
2. Run StartNewSession.py after setting the Chrome options, especially proxy and user-data-dir, via chrome_options.add_argument().
3. In ReUseForChrome.py file, specify the right location of file SessionInfo.txt at the line ```with open("F:\GitHub\lib_ChromeReuse\SessionInfo.txt", 'r') as f:```.
4. Run selenium_fetcher.py after specifying the right locaiton of file ReUseForChrome.py at the line [sys.path.append("F:\GitHub\lib_ChromeReuse")]
5. Run command [pyspider --phantomjs-proxy=http://localhost:9000 -c pyspidercon.json] to launch the Pyspider, where pyspidercon.json is a config file to contain at least the following:
{
  "fetcher":{
	"poolsize":1
  }
}
.This config file makes Pyspider to crawl websites one by one.
6. To use Chrome+Selenium in Pyspider, write crawl function like: self.crawl('url', callback=callback_function, fetch_type='js',js_script={'1':str1,'2':str2}), where str1 and str2 is the Python code running before and after the code [driver.get(fetch['url'])] in selenium_fetcher.py, respectively. Please see the selenium_fetcher.py and GooglePatent.py for details.

### About GooglePatent.py
GooglePatent.py is the source code which can run in Pyspider to use Chrome+Selenium to crawl GooglePatent. Enjoy it!
