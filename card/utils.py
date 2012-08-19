from bs4 import BeautifulSoup as bs
from re import compile, sub
import urllib, urllib2
import os
import json

def get_link(id):
    dc = get_web('cardid=%s' % id)
    link = get_data_link(dc)
    if link:
        return '/'.join(['http://imperialassembly.com/oracle', link])
    return None

def get_cards(limit, offset=1):
    for i in range(offset, limit):
        cfilename = 'card_%d.data' % i
        ifilename = 'card_%d.jpeg' % i
        c = 'cardid=%d' % i     
        print c,
        dc = get_web(c)
        card = get_data(dc)
        if not card:
            continue
        card['id'] = i
        if 'last_set' in card:
            folder = os.path.join('cards', card['last_set'])
        else:
            folder = os.path.join('cards', 'unknown')
        imgfolder = os.path.join(folder, 'img')
        di = get_img(card['img'])
        if len(di) == 0:
            with open('checkout.fail', 'a') as f:
                f.write(c)
            print 'No %s' % c
        if not os.path.isdir(imgfolder):
            os.makedirs(imgfolder)
        with open(os.path.join(imgfolder, ifilename), 'w') as f:
            f.write(di)
        if 'cnids' in card:
            for si, cn in enumerate(card['cnids']):
                cnidi = get_img(card['img'], cn)
                cnidfile = 'card_%d__%d.jpeg' % (i, si)
                with open(os.path.join(imgfolder, cnidfile), 'w') as f:
                    f.write(cnidi)
            del card['cnids']
        del card['img']
        with open(os.path.join(folder, cfilename), 'w') as f:
            json.dump(card, f)
        print '... done'

def get_web(params):
    rq = urllib2.Request('http://imperialassembly.com/oracle/docard/', params)
    l = urllib2.urlopen(rq)
    return l.read()

def get_img(src, nestid=None):
    if nestid:
        src = sub('nestid=.*?&', 'nestid=%s&' % nestid, src)
        src = sub('&hash=.*', '', src)
    l = urllib2.urlopen('/'.join(['http://imperialassembly.com/oracle', src]))
    return l.read()

def get_data_link(data):
    soup = bs(data)
    try:
        return soup.find('img').get('src')
    except AttributeError:
        return None
    
def get_data(data):
    soup = bs(data, convertEntities=bs.HTML_ENTITIES)
    card = {}
    try:
        card['img'] = soup.find('img').get('src')
    except AttributeError:
        return None
    card['name'] = extract(soup, compile('^Card.*Title$'), 'string')
    card['cost'] = extract(soup, 'Cost', 'text')
    card['text'] = extract (soup, 'Text')
    if card['text']:
        card['text'] = card['text'].renderContents()
    card['flavor'] = extract(soup, compile('^Flavor.*Text$'))
    if card['flavor']:
        card['flavor'] = card['flavor'].renderContents()
    card['focus'] = extract(soup, compile('^Focus.*Value$'), 'text')
    card['number'] = extract(soup, compile('^Card.*Number$'), 'string')
    card['type'] = extract(soup, compile('^Card.*Type$'), 'string')
    card['rarity'] = extract(soup, 'Rarity', 'string')
    card['legality'] = extract(soup, 'Legality', 'string')
    if card['legality']:
        card['legality'] = [l.strip() for l in 
            card['legality'].replace(u'\xa0', ' ').split(u'\x95')]
    card['set'] = extract(soup, 'Set')
    if card['set']:
        card['others'] = card['set'].findAll('a')
        if card['others']:
            card['other_sets'] = [s.string.replace(u'\u2013', ' - ') 
                                    for s in card['others']]
            card['cnids'] = [s.get('href').split('cnidprinting=')[1].split('&')[0]
                                    for s in card['others']]
        card['last_set'] = card['set'].find('span')
        if not card['last_set']:
            for cs in card['set'].findChildren():
                cs.extract()
            card['last_set'] = card['set']
        card['last_set'] = card['last_set'].text.replace(u'\u2013', ' - ')
        card['last_set'] = card['last_set'].replace(u'\x95', '').strip()
    card['set'] = None
    card['others'] = None
    card['keywords'] = extract(soup, 'Keywords')
    if card['keywords']:
        card['keywords'] = [k.string for k in card['keywords'].findAll('b')]
    card['errata'] = extract(soup, compile('^Errata.*MRP$'))
    if card['errata']:
        card['errata'] = card['errata'].renderContents()
    card['force'] = extract(soup, compile('^Force.*Chi$'), 'next')
    if card['force']:
        card['chi'] = card['force'].find(attrs='chi').string
        card['force'] = card['force'].find(attrs='force').string
    card['ps'] = extract(soup, compile('^PS.*GP.*.SH$'), weird=True)
    if card['ps']:
        card['gp'] = card['ps'].find(attrs='gc').next
        card['sh'] = card['ps'].find(attrs='hr').next
        card['ps'] = card['ps'].find(attrs='force').next
    card['hr'] = extract(soup, compile('^HR.*GC.*.PH$'), weird=True)
    if card['hr']:
        card['ph'] = card['hr'].find(attrs='ph').next
        card['cost'] = card['hr'].find(attrs='gc').next
        card['hr'] = card['hr'].find(attrs='hr').next
    card['clan'] = extract(soup, 'Clan', 'string')
    if card['clan']:
        card['clan'] = [c.strip() for c in card['clan'].split(u'\x95')]
    for key in card.keys():
        if not card[key]:
            del card[key]
    return card

def extract(data, text, placement=[], weird=False):
    if isinstance(placement, str):
        placement = placement.split('.')
    ext = data.find(text=text)
    if not ext:
        return None
    else:
        ext = ext.parent.parent.nextSibling.next if not weird else ext.parent.parent.parent.nextSibling.next
        for att in placement:
            ext = getattr(ext, att)
        return ext

def make_sets():
    to_delete = []
    all_cards = {}
    for d in os.listdir('.'):
        cards = {}
        for f in os.listdir(d):
            if 'card' in f:
                with open(os.path.join(d, f)) as fd:
                    card = json.load(fd)
                    if len(card) == 1:
                        to_delete.append(card['id'])
                        continue
                    cards[card['id']] = card
                        
        with open(os.path.join(d, 'set.data'), 'w') as fd:
            json.dump(cards, fd)
        all_cards.update(cards)
    with open('total.data', 'w') as fd:
        json.dump(all_cards, fd)
    for i in to_delete:
        os.system("rm -rf */card_%s\.*" % i)
        os.system("rm -rf */*/card_%s\.*" % i)

