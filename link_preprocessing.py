import re
from typing import List

AD_LINKS = ['doubleclick.net',
            'googleads.g.doubleclick.net',
            'ad.mail.ru',
            'click.mail.ru',
            'ru.mail.mailapp.files',
            'googleads.github.io',
            'vk.link',
            'avatars.mds.yandex.net',
            'yastatic.net',
            'i.ytimg.com',
            'relap.io',
            'banners.adfox.ru',
            'ads.adfox.ru',
            'syndication.realsrv.com',
            'ssp.otm-r.com',
            'ads.betweendigital.com',
            's.optnx.com',
            'dsp.rtb.mts.ru',
            'tpc.googlesyndication.com',
            's.viiadr.com',
            'rtb.com.ru',
            'exchange.buzzoola.com',
            'ad.adriver.ru'
            ]

BAD_PREFIXES = [
    '^m\.',
    '^t\.',
    '^webattach\.',
    '^android\.',
    '^epg\.',
    '^g\.',
    '^connect\.',
    '^away\.',
    '^id\.',
    '^ad\.',
    '^ads\.',
    '^crucia\.',
    '^online\.',
    '^web\d*\.',
    '^node\d*\.',
    '^i\.',
    '^banners\.',
    '^login\.'
]

bad_postfixes = [
]


class LinkCleaner():
    def __init__(self,
                 ad_links: List[str],
                 bad_prefixes: List):
        self.ad_links = ad_links
        self.prefixes = bad_prefixes
        self.locations = {}

    def clean_location(self, link):
        parts = link.split('.')
        no_loc_link = '.'.join(parts[:-1])
        if not no_loc_link in self.locations:
            self.locations[no_loc_link] = parts[-1]
        return f'{no_loc_link}.{self.locations[no_loc_link]}'

    def clean_site_platform(self, link):
        for prefix in self.prefixes:
            link = re.sub(prefix, '', link)
        if re.match(r'^vk\.[^\.]+\.', link):
            link = link[3:]
        if re.match(r'^mail\.[^\.]+\.*', link):
            link = link[5:]
        return link

    def clean_advertisment(self, link):
        if link in self.ad_links:
            return "[advertisment]"
        if re.search(r'\.otm-r\.', link):
            return "[advertisment]"
        return link

    def parse_yandex(self, link):
        if re.match('app-\d+\.games\.s3\.yandex\.net', link):
            app_id = re.search(r'\d+', link).group(0)
            return f'yandex.ru/games/app/{app_id}'
        return link

    def clean_extras(self, link):
        link = re.sub(r'sun\d+-\d+.userapi.*', 'vk.com', link)
        link = re.sub(r'yandex\.direct-24\.*', 'direct.yandex.ru', link)
        link = re.sub(r'yabro1\.zen-test\.yandex.*', 'yandex.ru', link)
        link = re.sub(r'yandex\.browser\.ideaprog\.download', 'yandex.ru', link)
        link = re.sub(r'znakomstva\.love\.mail.*', 'love\.mail\.ru', link)
        return link

    def clean_speeders(self, link):
        if re.match(r'\.turbopages\.org$', link):
            link = re.sub(r'-', '.', link)
            link = re.sub(r'\.\.', '-', link)
        return link

    def clean_link(self, link):
        link = self.clean_speeders(link)
        link = self.clean_location(link)
        link = self.clean_advertisment(link)
        link = self.clean_site_platform(link)
        link = self.parse_yandex(link)
        link = self.clean_extras(link)
        return link

# USAGE EXAMPLE
cleaner = LinkCleaner(AD_LINKS, BAD_PREFIXES)
print(cleaner.clean_link('mail.yandex.ru'))
