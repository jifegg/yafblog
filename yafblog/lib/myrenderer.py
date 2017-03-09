import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

class MyRenderer(mistune.Renderer):
    def block_code(self, text, lang):
        linenos = inlinestyles = False
        if not lang:
            text = text.strip()
            return u'<pre><code>%s</code></pre>\n' % mistune.escape(text)

        try:
            lexer = get_lexer_by_name(lang, stripall=True)
            formatter = HtmlFormatter(
                noclasses=inlinestyles, linenos=linenos, cssclass='codehilite'
            )
            code = highlight(text, lexer, formatter)
            if linenos:
                return '<div class="highlight-wrapper">%s</div>\n' % code
            return '<div class="doc doc-code">%s</div>%s' % (lang.upper(), code)
        except:
            return '<pre class="%s"><code>%s</code></pre>\n' % (
                lang, mistune.escape(text)
            )

    def link(self, link, title, text):
        link = mistune.escape_link(link)
        if not title:
            return '<a href="%s" target="_blank">%s</a>' % (link, text)
        title = escape(title, quote=True)
        return '<a href="%s" title="%s" target="_blank">%s</a>' % (link, title, text)

    def header(self, text, level, raw=None):
        rv = '<h%d id="toc-%d">%s</h%d>\n' % (
            level, self.toc_count, text, level
        )
        self.toc_tree.append((self.toc_count, text, level, raw))
        self.toc_count += 1
        return rv

    def reset_toc(self):
        self.toc_tree = []
        self.toc_count = 0

    def render_toc(self, level=3):
        """Render TOC to HTML.
        :param level: render toc to the given level
        """
        return ''.join(self._iter_toc(level))

    def _iter_toc(self, level):
        first_level = None
        last_level = None

        yield '<ul id="table-of-content">\n'

        for toc in self.toc_tree:
            index, text, l, raw = toc

            if l > level or l < 2:
                # ignore this level
                continue

            if first_level is None:
                # based on first level
                first_level = l
                last_level = l
                yield '<li><a href="#toc-%d">%s</a>' % (index, text)
            elif last_level == l:
                yield '</li>\n<li><a href="#toc-%d">%s</a>' % (index, text)
            elif last_level == l - 1:
                last_level = l
                yield '<ul>\n<li><a href="#toc-%d">%s</a>' % (index, text)
            elif last_level > l:
                # close indention
                yield '</li>'
                while last_level > l:
                    yield '</ul>\n</li>\n'
                    last_level -= 1
                yield '<li><a href="#toc-%d">%s</a>' % (index, text)

        # close tags
        if first_level and last_level:
            yield '</li>\n'
            while last_level > first_level:
                yield '</ul>\n</li>\n'
                last_level -= 1

        yield '</ul>\n'
