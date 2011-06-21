
URLS = [
    'http://api.dribbble.com/shots/everyone',
    'http://api.dribbble.com/shots/debuts',
    'http://api.dribbble.com/shots/popular'
]
FILTER = r'(san francisco)|(sf[ ,])|(oakland)|(berkeley)|(palo alto)|(mountain view)|(bay area)|(california)|(silicon)'

import simplejson as json
import urllib2, urllib, time, re, codecs

FILTER = re.compile(FILTER)

def to_unicode(s, encoding='utf-8'):
    """convert any value to unicode, except None"""
    if s is None:
        return None
    if isinstance(s, unicode):
        return s
    if isinstance(s, str):
        return s.decode(encoding, 'ignore')
    return unicode(s)

def csv_out(data, out):
    FIELDS = ["id", "name", "url", "location", "website_url",
              "twitter_screen_name", "shots_count", "followers_count"]
    
    lines = [','.join(FIELDS)]
    for id, p in data.items():
        lines.append(u','.join([f in p and to_unicode(p[f]) or u'Unknown' for f in FIELDS]))
    
    csv = codecs.open(out, 'w', 'utf-8')
    for l in lines:
        l = l+u'\n'
        csv.write(l)
    csv.close()

def filter(dude):
    
    if dude['location'] and FILTER.search(dude['location'].lower()):
        dude['location'] = dude['location'].replace(',', '')
        return True
    return False
    #return True

def _main(out):
    dudes = {}
    
    for url in URLS:
        p_data = {
            'page': 1,
            'per_page': 30
        }
        
        pages = 1000
        
        while p_data['page'] <= pages:
            s = urllib2.urlopen('%s?%s' % (url, urllib.urlencode(p_data))).read()
            try:
                s = json.loads(s)
            except:
                print "FAIL loading json %s" % s
                break
            
            pages = s['pages']
            p_data['page'] = s['page']+1
            
            players = [shot['player'] for shot in s['shots']]
            
            print [(p['username'], p['location']) for p in players]
            
            for p in players:
                if filter(p):
                    dudes[p['id']] = p
            
            time.sleep(1)
    
    csv_out(dudes, out)

if __name__ == '__main__':
    import sys
    _main(*sys.argv[1:])

