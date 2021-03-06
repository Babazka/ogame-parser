#! coding: utf-8
import re
from cStringIO import StringIO

import requests
import lxml.html
import lxml.etree

import local_config
import formulas


def parse_html(string):
    parser = lxml.html.HTMLParser(encoding='utf-8')
    html = lxml.html.parse(StringIO(string.encode('utf-8')), parser=parser).getroot()
    return html


def parse_int(string):
    if u'М' in string:  # Миллионы
        return int(float(string.strip()[:-1]) * 1000000)

    return int(string.strip().replace('.', ''))


def rjust_int(v):
    if isinstance(v, int):
        return '%7d' % v
    return str(v)


RESOURCES = ['metal', 'crystal', 'deuterium']

RESOURCES_RU = [u'Рудник по добыче металла', u'Рудник по добыче кристалла', u'Синтезатор дейтерия']

TRANSPORT_CAPACITY = {
    u'Большой транспорт': 25000,
    u'Малый транспорт': 5000,
}

MILITARY_SHIPS = [
    u'Лёгкий истребитель',
    u'Тяжёлый истребитель',
    u'Крейсер',
    u'Линкор',
    u'Линейный крейсер',
    u'Бомбардировщик',
    u'Уничтожитель',
    u'Звезда смерти',
]
TRANSPORT_SHIPS = [
    u'Малый транспорт',
    u'Большой транспорт',
]
BIG_TRANSPORT = TRANSPORT_SHIPS[-1]
UTILITY_SHIPS = [
    u'Колонизатор',
    u'Переработчик',
    u'Шпионский зонд',
]

SHIPS = MILITARY_SHIPS + TRANSPORT_SHIPS + UTILITY_SHIPS

SHIP_ABBRS = {
    u'Лёгкий истребитель': u'ЛИ',
    u'Тяжёлый истребитель': u'ТИ',
    u'Крейсер': u'КРЕЙ',
    u'Линкор': u'ЛИНК',
    u'Линейный крейсер': u'Л.КРЕЙ',
    u'Бомбардировщик': u'БОМБ',
    u'Уничтожитель': u'УНИК',
    u'Звезда смерти': u'ЗС',
    u'Малый транспорт': u'МТ',
    u'Большой транспорт': u'БТ',
    u'Колонизатор': u'КЛНЗ',
    u'Переработчик': u'ПЕРЕ',
    u'Шпионский зонд': u'ШП',
}



class Planet(object):
    def __init__(self, name, coords, planetid, parser):
        self.name = name
        self.coords = coords
        self.planetid = planetid
        self.parser = parser
        self.resources = None
        self.fleet = None

    def fetch_resources(self):
        #return open('resources.html').read().decode('utf-8')

        r = self.parser.session.get(local_config.SERVER + '/game/index.php?page=resourceSettings&cp=' + str(self.planetid))
        with open('resources.html', 'w') as f:
            f.write(r.text.encode('utf-8'))
        return r.text

    def parse_resources(self):
        if self.resources is not None:
            return
        html = parse_html(self.fetch_resources())
        resources = {}
        for kind in RESOURCES + ['energy']:
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

            m = re.match(ur'^(.*?)\s+\(Уровень\s+(\d+)\)$', tds[0])
            if m:
                for ru_kind, kind in zip(RESOURCES_RU, RESOURCES):
                    if m.group(1) == ru_kind:
                        resources[kind]['level'] = parse_int(m.group(2))
                if m.group(1) == u'Солнечная электростанция':
                    resources['energy']['level'] = parse_int(m.group(2))

            if tds[0] == u'Вместимость хранилищ':
                for kind, v in zip(RESOURCES, tds[1:]):
                    resources[kind]['capacity'] = parse_int(v)
            if tds[0] == u'Выработка в час:':
                for kind, v in zip(RESOURCES, tds[1:]):
                    resources[kind]['per_hour'] = parse_int(v)
        self.resources = resources

    def next_level(self, kind):
        cur_lvl = self.resources[kind]['level']
        m, c = formulas.build_price(kind, cur_lvl + 1)
        e_cur = formulas.energy_consumption(kind, cur_lvl)
        e_new = formulas.energy_consumption(kind, cur_lvl + 1)
        e_delta = e_new - e_cur
        dm = m - self.resources['metal']['current']
        dc = c - self.resources['crystal']['current']
        dm = max(0, dm)
        dc = max(0, dc)
        de = -e_delta - self.resources['energy']['current']
        de = max(0, de)
        return [
            ('next lvl', '%s mt %s cr' % (rjust_int(m), rjust_int(c))),
            ('need',     '%s mt %s cr %s dE' % (rjust_int(dm), rjust_int(dc), rjust_int(de))),
        ]

    def dump_resources(self):
        def print_line(kind, line):
            print '\t' + kind.ljust(9) + '\t' + '\t'.join(map(rjust_int, line))

        for kind in RESOURCES + ['energy']:
            line = []
            for k, v in self.resources[kind].iteritems():
                line.append(k)
                line.append(v)
            for k, v in self.next_level(kind):
                line.append(k)
                line.append(v)

            print_line(kind, line)

    def level_summary_line(self):
        line = []
        for kind in RESOURCES + ['energy']:
            line.append(self.resources[kind]['level'])
        return line

    def resource_summary_line(self):
        line = []
        for kind in RESOURCES:
            line.append(self.resources[kind]['current'])
        line.append(self.get_big_transport_capacity())
        return line

    def fetch_fleet(self):
        #return open('fleet.html').read().decode('utf-8')

        r = self.parser.session.get(local_config.SERVER + '/game/index.php?page=fleet1&cp=' + str(self.planetid))
        with open('fleet.html', 'w') as f:
            f.write(r.text.encode('utf-8'))
        return r.text

    def parse_fleet(self):
        if self.fleet is not None:
            return
        html = parse_html(self.fetch_fleet())
        fleet = {}
        for el in html.cssselect('form#shipsChosen div.buildingimg a'):
            title = el.cssselect('span.textlabel')[0].text.strip()
            number = parse_int(el.cssselect('span.textlabel')[0].tail)
            if number == 0:
                continue
            fleet[title] = number
        self.fleet = fleet

    def dump_fleet(self):
        for group in [MILITARY_SHIPS, TRANSPORT_SHIPS, UTILITY_SHIPS]:
            line = []
            transport_capacity = 0
            for kind in group:
                if kind in self.fleet:
                    n = self.fleet[kind]
                    abbr = SHIP_ABBRS[kind]
                    line.append(u'%s: %s' % (kind, n))
                    transport_capacity += n * TRANSPORT_CAPACITY.get(kind, 0)
            if transport_capacity > 0:
                line.append(u'Ёмкость: %d' % transport_capacity)
            if line:
                print '\t' + '\t'.join(line)

    def get_big_transport_capacity(self):
        capacity = self.fleet.get(BIG_TRANSPORT, 0) * TRANSPORT_CAPACITY.get(BIG_TRANSPORT, 0)
        return capacity

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

    def resource_overview(self):
        totals = {kind: {'per_hour': 0, 'current': 0} for kind in RESOURCES}
        for planet in self.planets:
            planet.parse_resources()
            print planet
            planet.dump_resources()
            for kind in RESOURCES:
                totals[kind]['per_hour'] += planet.resources[kind]['per_hour']
                totals[kind]['current'] += planet.resources[kind]['current']
        print 'TOTAL:'
        for kind in RESOURCES:
            print '\t', totals[kind]

    def fleet_overview(self):
        totals = {kind: 0 for kind in SHIPS}
        for planet in self.planets:
            planet.parse_fleet()
            print planet
            planet.dump_fleet()
            for kind in SHIPS:
                totals[kind] += planet.fleet.get(kind, 0)
        print 'TOTAL:'
        for kind in SHIPS:
            if totals[kind] > 0:
                print '\t', kind, totals[kind]

    def resource_and_fleet_overview(self):
        resource_totals = {kind: {'per_hour': 0, 'current': 0} for kind in RESOURCES}
        ship_totals = {kind: 0 for kind in SHIPS}

        res_summary = []
        level_summary = []

        for planet in self.planets:
            planet.parse_resources()
            planet.parse_fleet()
            print planet
            planet.dump_resources()
            for kind in RESOURCES:
                resource_totals[kind]['per_hour'] += planet.resources[kind]['per_hour']
                resource_totals[kind]['current'] += planet.resources[kind]['current']
            planet.dump_fleet()
            for kind in SHIPS:
                ship_totals[kind] += planet.fleet.get(kind, 0)
            print ''
            level_summary.append([planet.name] + planet.level_summary_line())
            res_summary.append([planet.name] + planet.resource_summary_line())

        print 'CURRENT RESOURCES:'
        print '%20s' % 'planet',
        for header in RESOURCES + ['big_transport_capacity']:
            print '%10s' % header,
        print ''
        for line in res_summary:
            print '%20s' % line[0],
            for item in line[1:]:
                print '%10s' % item,
            print ''
        print ''

        print 'LEVELS:'
        print '%20s' % 'planet',
        for header in RESOURCES + ['energy']:
            print '%10s' % header,
        print ''
        for line in level_summary:
            print '%20s' % line[0],
            for item in line[1:]:
                print '%10s' % item,
            print ''
        print ''


        print 'TOTAL:'
        for kind in RESOURCES:
            line = []
            for k, v in resource_totals[kind].iteritems():
                line.append(k)
                line.append(v)
            line.append('per_day')
            line.append(rjust_int(resource_totals[kind]['per_hour'] * 24))
            print '\t' + kind.ljust(9) + '\t' + '\t'.join(map(rjust_int, line))
        for kind in SHIPS:
            if ship_totals[kind] > 0:
                print '\t', kind, ship_totals[kind]


if __name__ == '__main__':
    parser = Parser()
    parser.login()
    #parser.resource_overview()
    #parser.parse_first_screen()
    parser.resource_and_fleet_overview()
