import misaka as md
import houdini as h
import os
import pygments
import latex2markdown
from PySide import QtWebKit, QtCore
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from bs4 import BeautifulSoup
from Config import config
from mdfilemodel import MdFileModel


class HighlightRenderer(md.HtmlRenderer, md.SmartyPants):

    def block_code(self, text, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                h.escape_html(text.strip())
        if str(lang).strip() == 'latex-block':
            md_str = latex2markdown.LaTeX2Markdown(text).to_markdown()
            return md_str

        try:
            lexer = get_lexer_by_name(lang, stripall=True)
            formatter = HtmlFormatter()
            return highlight(text, lexer, formatter)
        except pygments.util.ClassNotFound:
            return '\n<pre><code>%s</code></pre>\n' % \
                h.escape_html(text.strip())


class MarkdownView(QtWebKit.QWebView):

    """ Render the markdown with specific style. """
    mdTitleChanged = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(MarkdownView, self).__init__(parent)
        self.renderer = HighlightRenderer()
        self.style_path = config.get_style_path()
        self.highlight_path = config.get_highlight_path()
        self.m_mdFile = None
        self.setHtml("<h1>Welcome to Markdown viewer</h1>")
        self.header = "Untitled"

    def setMarkdown(self, md_str):
        md_renderer = md.Markdown(self.renderer,
                                  extensions=md.EXT_FENCED_CODE |
                                  md.EXT_NO_INTRA_EMPHASIS)
        html = self.render(md_renderer.render(md_str))
        QtWebKit.QWebView.setHtml(self, html,
                                  baseUrl=QtCore.QUrl('file://' +
                                                      self.m_mdFile.absPath()))

    def loadMd(self, filePath):
        self.m_mdFile = MdFileModel(filePath)
        self.m_mdFile.fileModified.connect(self.onMdFileModified)
        self.reload()

    def reload(self):
        if self.m_mdFile is None:
            return
        oldScrollPos = self.page().mainFrame().scrollPosition()
        md_str = self.m_mdFile.read()
        self.setMarkdown(md_str)
        self.page().mainFrame().setScrollPosition(oldScrollPos)

    def render(self, html):
        soup = BeautifulSoup(html)
        self._setCss(soup)
        self._setMathJax(soup)
        self._fixImg(soup)
        header = soup.body.h1.string
        if header is not None or header != '':
            self.header = soup.body.h1.string
            self.mdTitleChanged.emit(self.header)
        print(soup.prettify())
        return str(soup)

    def getMdTitleText(self):
        return self.header

    def onMdFileModified(self):
        self.reload()

    def _fixImg(self, soup):
        for img in soup.find_all('img'):
            src = img['src']
            src = "file://" + os.path.join(self.m_mdFile.absPath(), src)
            img['src'] = src

    def _setCss(self, soup):
        head_tag = soup.new_tag('head')

        style_tag = self._createCss(soup, self.style_path)
        head_tag.append(style_tag)

        highlight_tag = self._createCss(soup, self.highlight_path)
        head_tag.append(highlight_tag)

        soup.html.body.insert_before(head_tag)
        main_div_tag = soup.html.body
        main_div_tag.name = 'div'
        main_div_tag['id'] = 'main'
        main_div_tag.wrap(soup.new_tag('body'))

    def _createCss(self, soup, href):
        link_tag = soup.new_tag("link")
        link_tag['media'] = 'screen'
        link_tag['rel'] = 'stylesheet'
        link_tag['type'] = 'text/css'
        link_tag['href'] = href
        return link_tag

    def _setMathJax(self, soup):
        mathjax_script1 = """
<script type="text/x-mathjax-config">
MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]}});
</script>
"""
        mathjax_script2 = """
<script type="text/javascript"
src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
</script>
        """
        script_tag1 = \
            BeautifulSoup(mathjax_script1).html.head.script
        script_tag2 = \
            BeautifulSoup(mathjax_script2).html.head.script
        print(script_tag1)
        print(script_tag2)
        soup.head.append(script_tag1)
        soup.head.append(script_tag2)
