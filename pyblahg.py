#!/usr/bin/python2

from __future__ import unicode_literals

import time
from glob import glob

import markdown
import yaml

# load template files
with open("post.template") as t:
    template = t.read()
with open("index.template") as i:
    index = i.read()


class Post(object):
    def __init__(self, title, content, date = None):
        self.title = title
        self.content = content
        self.time = time.time() if date == None else date


def post2html(post):
    return template.format(
            title = post.title,
            time = time.asctime(time.gmtime(post.time)),
            content = markdown.markdown(post.content))

def yaml2post(yamlfile):
    with open(yamlfile) as f:
        post = yaml.load(f.read())
    return post

def post2yaml(post, yamlfile):
    with open(yamlfile, 'w') as f:
        f.write(yaml.dump(post))

def loadPosts(folder):
    if not folder.endswith('/'):
        folder += "/"
    files = glob("{0}*.yaml".format(folder))
    posts = []
    for f in files:
        posts.append(yaml2post(f))
    return posts

def makeBlahg():
    posts = loadPosts("posts/")
    posts = sorted(posts, key=lambda p : p.time, reverse=True)
    html = '\n'.join([ post2html(p) for p in posts ])
    with open("index.html", 'w') as i:
        i.write(index.format(body = html))

if __name__ == "__main__":
    makeBlahg()
