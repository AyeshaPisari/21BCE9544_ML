import threading
import time
# background processing
def scrape_news():
    while True:
        print("Scraping...")
        time.sleep(60)  

# Starting the background thread
thread = threading.Thread(target=scrape_news)
thread.daemon = True
thread.start()
