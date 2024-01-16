import scrapy
import re as regex

class Shrek1SpiderSpider(scrapy.Spider):
    name = "shrek1_spider"
    allowed_domains = ["shrek.fandom.com"]
    start_urls = ["https://shrek.fandom.com/wiki/Shrek_(film)/Transcript"]

    def parse(self, response):
        '''
        Scraping and parsing logic:
        1. Scrap only the script elements inside script div;
        2. Only keep elements after (non-incl) h# elements;
        3. Check if script piece is dialog, setting, or action;
        4. Parse and lable each accordingly with yield.
        '''

        s_list = response.css('div.mw-parser-output > *')
        
        # Skip until transcript starts (third child):
        start_idx = 2
        end_over = len(s_list)

        for i in range(start_idx, end_over, 1):
            tmp_s = s_list[i]
            content = ''.join(tmp_s.css('::text').getall()).strip()
            
            # Check for dialog (speaker: content):
            if regex.match(r'[^:]+:', content):
                spk_con =  content.split(': ', maxsplit=1)
                yield{
                    'position' : i,
                    'content' : spk_con[-1].strip(),
                    'type' : 'dialog',
                    'speaker' : spk_con[0].strip(),
                }
            # Check for action (starts and ends with '()'):
            elif regex.match(r'^[(].+[)]$', content):
                yield{
                    'position' : i,
                    'content' : content,
                    'type' : 'action',
                    'speaker' : None,
                }
            # Otherwise it's setting text:
            else:
                yield{
                    'position' : i,
                    'content' : content,
                    'type' : 'setting',
                    'speaker' : None,
                }
