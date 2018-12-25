import requests
from bs4 import BeautifulSoup

url_tpl = 'http://mvnrepository.com/artifact/{0}/{1}'

headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'http://mvnrepository.com/',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Cookie': '_ga=GA1.2.1147991867.1528446514; _gid=GA1.2.1637047582.1536829109; _gat=1; MVN_SESSION=eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7InVpZCI6IjUwNmY1MGIxLTk5NjEtMTFlOC04MmQwLWNmNjk0ZDVjMWU3NCJ9LCJleHAiOjE1NjgzNjYxNzUsIm5iZiI6MTUzNjgzMDE3NSwiaWF0IjoxNTM2ODMwMTc1fQ.RmSsdbHql3azXJOQvVJ1fz-EmXRwetdP8Jpys0KOxFc'
}


def load_version(group, artifact):
    print('')
    print(group, artifact)
    url = url_tpl.format(group, artifact)
    print(url)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser').select('table.versions > tbody')
    # analyse & format: only show top 6
    for version in soup[:3]:
        # only show release edition
        release = version.select('a.release')
        if len(release) == 0:
            continue
        # only show top 6
        release = release[:6]
        print(', '.join([a.text for a in release]))


def show_version():
    modules = [
        'com.alibaba:druid',
        'org.mybatis:mybatis',
        'mysql:mysql-connector-java',
        'com.alibaba:fastjson',
        'org.slf4j:slf4j-api',
        'ch.qos.logback:logback-classic',
        'org.projectlombok:lombok',
        'com.fasterxml.jackson.core:jackson-databind',
        'org.mockito:mockito-all',
        'org.springframework:spring-webmvc',
        'org.springframework:spring-tx',
        'org.springframework:spring-test',
        'org.springframework.boot:spring-boot-starter-web',
        'org.springframework.boot:spring-boot',
        'org.springframework.boot:spring-boot-starter-test',
        'org.mybatis.spring.boot:mybatis-spring-boot-starter',
        'com.alibaba:dubbo',
        'joda-time:joda-time',
        'com.github.pagehelper:pagehelper',
        'redis.clients:jedis',
        'org.freemarker:freemarker',
        'org.apache.shiro:shiro-web',
        'io.netty:netty-all',
        'org.ehcache:ehcache',
        'org.hibernate.validator:hibernate-validator',
    ]
    for md in modules:
        keys = md.split(':')
        load_version(keys[0], keys[1])


if __name__ == '__main__':
    show_version()
