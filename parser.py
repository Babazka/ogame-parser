#! coding: utf-8
import re
from cStringIO import StringIO

import requests
import lxml.html
import lxml.etree

import local_config


def parse_html(string):
    parser = lxml.html.HTMLParser(encoding='utf-8')
    html = lxml.html.parse(StringIO(string.encode('utf-8')), parser=parser).getroot()
    return html


def parse_int(string):
    return int(string.strip().replace('.', ''))


RESOURCES = ['metal', 'crystal', 'deuterium']
RESOURCES_RU = [u'металла', u'кристалла', u'дейтерия']


class Planet(object):
    def __init__(self, name, coords, planetid, parser):
        self.name = name
        self.coords = coords
        self.planetid = planetid
        self.parser = parser
        self.resources = {}

    def fetch_resources(self):
        #return open('resources.html').read().decode('utf-8')

        r = self.parser.session.get(local_config.SERVER + '/game/index.php?page=resourceSettings&cp=' + str(self.planetid))
        with open('resources.html', 'w') as f:
            f.write(r.text.encode('utf-8'))
        return r.text

    def parse_resources(self):
        html = parse_html(self.fetch_resources())
        resources = {}
        for kind in RESOURCES:
            res = {
                'level': 0,
                'current': 0,
                'per_hour': 0,
                'capacity': 0,
            }
            resources[kind] = res
            v = html.cssselect('#%s_box span.value span' % kind)[0]
            res['current'] = parse_int(v.text)

        for row in html.cssselect('table.listOfResourceSettingsPerPlanet tr'):
            tds = []
            for td in row.cssselect('td'):
                t = lxml.etree.tostring(td, method='text', encoding='utf-8').decode('utf-8')
                tds.append(t.strip())
            if not tds:
                continue

            m = re.match(ur'.*\s(\S+)\s+\(Уровень\s+(\d+)\)$', tds[0])
            if m:
                for ru_kind, kind in zip(RESOURCES_RU, RESOURCES):
                    if m.group(1) == ru_kind:
                        resources[kind]['level'] = parse_int(m.group(2))

            if tds[0] == u'Вместимость хранилищ':
                for kind, v in zip(RESOURCES, tds[1:]):
                    resources[kind]['capacity'] = parse_int(v)
            if tds[0] == u'Выработка в час:':
                for kind, v in zip(RESOURCES, tds[1:]):
                    resources[kind]['per_hour'] = parse_int(v)
        self.resources = resources

    def dump_resources(self):
        for kind in RESOURCES:
            print kind, self.resources[kind]

    def __repr__(self):
        return 'Planet(name="%s", coords="%s", planetid="%s")' % (self.name, self.coords, self.planetid)


class Parser():
    def __init__(self):
        self._session = None
        self.first_screen = None

        self.first_screen = open('first_screen.html').read().decode('utf-8')

    def login(self):
        print 'Logging in...'
        s = requests.Session()
        r = s.post(local_config.LOGIN_SERVER + '/main/login/', local_config.AUTH_PARAMS)
        self.first_screen = r.text
        with open('first_screen.html', 'w') as f:
            f.write(self.first_screen.encode('utf-8'))
        self.parse_first_screen()
        self._session = s

    @property
    def session(self):
        if not self._session:
            self.login()
        return self._session

    def parse_first_screen(self):
        html = parse_html(self.first_screen)

        planets = []

        for el in html.cssselect('#planetList a.planetlink'):
            title = el.attrib.get('title')
            m_title = re.match(r'^<B>(.*?) \[(.*)\].*', title)
            href = el.attrib.get('href')
            m_href = re.match('.*&cp=(\d+)$', href)

            p = Planet(m_title.group(1), m_title.group(2), m_href.group(1), self)
            planets.append(p)
        self.planets = planets


if __name__ == '__main__':
    parser = Parser()
    parser.login()
    for planet in parser.planets:
        planet.parse_resources()
        print planet
        planet.dump_resources()
