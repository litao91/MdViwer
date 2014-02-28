import misaka as md
import houdini as h
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
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter()
        return highlight(text, lexer, formatter)


class MarkdownView(QtWebKit.QWebView):

    """ Render the markdown with specific style. """
    mdTitleChanged = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(MarkdownView, self).__init__(parent)
        self.renderer = HighlightRenderer()
        self.style_path = config.get_style_path()
        self.m_mdFile = None
        self.setHtml("<h1> Hello Markdown view</h1>")
        self.header = "Untitled"

    def setMarkdown(self, md_str):
        md_renderer = md.Markdown(self.renderer,
                                  extensions=md.EXT_FENCED_CODE |
                                  md.EXT_NO_INTRA_EMPHASIS)
        html = self.render(md_renderer.render(md_str))
        QtWebKit.QWebView.setHtml(self, html)

    def loadMd(self, filePath):
        self.m_mdFile = MdFileModel(filePath)
        self.m_mdFile.fileModified.connect(self.onMdFileModified)
        self.reload()

    def reload(self):
        if self.m_mdFile is None:
            return
        print('reloading')
        oldScrollPos = self.page().mainFrame().scrollPosition()
        md_str = self.m_mdFile.read()
        self.setMarkdown(md_str)
        self.page().mainFrame().setScrollPosition(oldScrollPos)

    def render(self, html):
        soup = BeautifulSoup(html)
        soup = self.set_css(soup)
        header = soup.body.h1.string
        if header is not '' or header is not None:
            self.header = soup.body.h1.string
            self.mdTitleChanged.emit(self.header)
        return str(soup)

    def getMdTitleText(self):
        return self.header

    def onMdFileModified(self):
        self.reload()

    def set_css(self, soup):
        head_tag = soup.new_tag('head')
        link_tag = soup.new_tag("link")
        link_tag['media'] = 'screen'
        link_tag['rel'] = 'stylesheet'
        link_tag['type'] = 'text/css'
        link_tag['href'] = self.style_path
        head_tag.append(link_tag)
        soup.html.body.insert_before(head_tag)
        main_div_tag = soup.html.body
        main_div_tag.name = 'div'
        main_div_tag['id'] = 'main'
        main_div_tag.wrap(soup.new_tag('body'))
        return soup
