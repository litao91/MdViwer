import misaka as md
import houdini as h
import os
from PySide import QtWebKit
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from bs4 import BeautifulSoup


class HighlightRenderer(md.HtmlRenderer, md.SmartyPants):
    def block_code(self, text, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                h.escape_html(text.strip())
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter()
        return highlight(text, lexer, formatter)


class MarkdownView(QtWebKit.QWebView):

    def __init__(self):
        super(MarkdownView, self).__init__()
        self.renderer = HighlightRenderer()

    def setMarkdown(self, md_str):
        md_renderer = md.Markdown(self.renderer,
                                  extensions=md.EXT_FENCED_CODE |
                                  md.EXT_NO_INTRA_EMPHASIS)
        html = self.beautifyHtml(md_renderer.render(md_str))
        # path = os.getcwd()
        #QtWebKit.QWebView.settings(self).setUserStyleSheetUrl(
            #QtCore.QUrl.fromLocalFile(path + '/res/style.css'))
        QtWebKit.QWebView.setHtml(self, html)

    def beautifyHtml(self, html):
        soup = BeautifulSoup(html)
        head_tag = soup.new_tag('head')
        link_tag = soup.new_tag("link")
        link_tag['media'] = 'screen'
        link_tag['rel'] = 'stylesheet'
        link_tag['type'] = 'text/css'
        link_tag['href'] = 'file://' + os.getcwd() + '/res/style.css'
        head_tag.append(link_tag)
        soup.html.body.insert_before(head_tag)
        main_div_tag = soup.html.body
        main_div_tag.name = 'div'
        main_div_tag['id'] = 'main'
        main_div_tag.wrap(soup.new_tag('body'))
        # print(soup.prettify())
        return str(soup)
