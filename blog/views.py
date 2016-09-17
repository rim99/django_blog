from datetime import date
from django.shortcuts import render, get_object_or_404
from django.template import Context
from misaka import Markdown, HtmlRenderer
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
import houdini
from .models import Blogpost, Tag

POSTS_PER_PAGE = 9
LENGTH_OF_SUMMARY = 200
THIS_YEAR = date.today().year  # Manually restart the server every year
MARKDOWN_EXTENSIONS = (
     'autolink',
     'strikethrough',
     'underline',
     'tables',
     'fenced-code',
     'footnotes',
     'highlight',
     'quote',
     'superscript',
     'math',
     'space-headers',
     'math-explicit',
     'disable-indented-code'
)  # remove 'no-intra-emphasis'

def md_to_html(blog_content):
    '''str -> str,
    Parse Markdown content to HTML content.
    '''
    class HighlighterRenderer(HtmlRenderer):
         def blockcode(self, text, lang):
             pass
             if not lang:
                 return '\n<pre><code>{}</code></pre>\n'.format(
                      houdini.escape_html(text.strip()))
             lexer = get_lexer_by_name(lang, stripall=True)
             formatter = HtmlFormatter()
             return highlight(text, lexer, formatter)
    rndr = HighlighterRenderer()
    md = Markdown(rndr, MARKDOWN_EXTENSIONS)
    content_html = (md(blog_content))
    return content_html

class Page_Info(object):
    '''This class contains some infomation about the posts list page:
    1. its page number
    2. whether it has next page or previous page
    3. its posts list
    '''
    def __init__(self, page_type='', current_page=1,
                 has_previous=False, has_next=False):
        self.page_type = page_type
        self.page = current_page
        self.has_previous = has_previous
        self.has_next = has_next
        self.post_list = []

    @classmethod
    def create(cls, page_type, page, all_blog_posts):
        def get_summary(post_list):
            for post in post_list:
                digest = post.content[:LENGTH_OF_SUMMARY]
                post.content = md_to_html(digest)
            return post_list
        page_num = int(page)
        start_count = (page_num - 1) * POSTS_PER_PAGE
        end_count = page_num * POSTS_PER_PAGE
        blog_posts = all_blog_posts[start_count:end_count]
        page_info = Page_Info(page_type, page_num, False, False)
        if page_num > 1:
            page_info.has_previous = True
        if end_count < len(all_blog_posts):
            page_info.has_next = True
        if page_info.page_type != 'archive':
            blog_posts=get_summary(blog_posts)
        page_info.post_list = blog_posts
        return page_info

def index(request, page_num=1):
    all_blog_posts = Blogpost.objects.all().order_by('pub_date')
    page_info = Page_Info.create('index', page_num, all_blog_posts)
    return render(request, 'home.html', {'page_info':page_info})

def archive(request, year=THIS_YEAR, page_num=1):
    all_blog_posts = Blogpost.objects.filter(pub_date__year=year).order_by('-pub_date')
    page_info = Page_Info.create('archive', page_num, all_blog_posts)
    return render(request, 'home.html', {'page_info':page_info})

def tag(request, tag, page_num=1):
    tag = Tag.objects.get(tag=tag)
    all_blog_posts = Blogpost.objects.filter(tag=tag).order_by('-pub_date')
    page_info = Page_Info.create('tag', page_num, all_blog_posts)
    return render(request, 'home.html', {'page_info':page_info})

def detail(request, blog):
    blog_post = get_object_or_404(Blogpost, blog_id=blog)
    blog_post.content = md_to_html(blog_post.content)
    blog_post.tag_name = blog_post.tag.all()[0].tag
    #render
    return render(request, 'post.html', {'post':blog_post})


