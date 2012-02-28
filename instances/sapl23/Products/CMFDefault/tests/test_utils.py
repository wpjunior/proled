from unittest import TestCase, makeSuite, main
import Testing
try:
    import Zope2
except ImportError: # BBB: for Zope 2.7
    import Zope as Zope2
Zope2.startup()

from Products.CMFCore.tests.base.content import FAUX_HTML_LEADING_TEXT
from Products.CMFCore.tests.base.content import SIMPLE_HTML
from Products.CMFCore.tests.base.content import SIMPLE_STRUCTUREDTEXT
from Products.CMFCore.tests.base.content import SIMPLE_XHTML
from Products.CMFCore.tests.base.content import STX_WITH_HTML


class DefaultUtilsTests(TestCase):
    COMMON_HEADERS = '''Author: Tres Seaver
Title: Test Products.CMFDefault.utils.parseHeadersBody'''

    MULTILINE_DESCRIPTION = '''Description: this description spans
        multiple lines.'''

    MULTIPARAGRAPH_DESCRIPTION = \
        '''Description: this description spans multiple lines.
        
        It includes a second paragraph'''

    TEST_BODY = '''Body goes here, and can span multiple
lines.  It can even include "headerish" lines, like:

Header: value
'''

    def test_parseHeadersBody_no_body( self ):
        from Products.CMFDefault.utils import parseHeadersBody

        headers, body = parseHeadersBody( '%s\n\n' % self.COMMON_HEADERS )
        self.assertEqual( len( headers ), 2 )
        self.failUnless( 'Author' in headers.keys() )
        self.assertEqual( headers[ 'Author' ], 'Tres Seaver' )
        self.failUnless( 'Title' in headers.keys() )
        self.assertEqual( len( body ), 0 )

    def test_parseHeadersBody_continuation( self ):
        from Products.CMFDefault.utils import parseHeadersBody

        headers, body = parseHeadersBody( '%s\n%s\n\n'
                                        % ( self.COMMON_HEADERS
                                          , self.MULTILINE_DESCRIPTION
                                          )
                                        )
        self.assertEqual( len( headers ), 3 )
        self.failUnless( 'Description' in headers.keys() )
        desc_len = len( headers[ 'Description' ].split('\n') )
        self.assertEqual( desc_len, 2 )
        self.assertEqual( len( body ), 0 )

    def test_parseHeadersBody_embedded_blank_line( self ):
        from Products.CMFDefault.utils import parseHeadersBody

        headers, body = parseHeadersBody( '%s\n%s\n\n%s'
                                        % ( self.COMMON_HEADERS
                                          , self.MULTIPARAGRAPH_DESCRIPTION
                                          , self.TEST_BODY
                                          )
                                        )
        self.assertEqual( len( headers ), 3 )
        self.failUnless( 'Description' in headers.keys() )
        desc_lines = headers[ 'Description' ].split('\n')
        desc_len = len( desc_lines )
        self.assertEqual( desc_len, 3, desc_lines )
        self.assertEqual( desc_lines[1], ' ' )
        self.assertEqual( body, self.TEST_BODY )

    def test_parseHeadersBody_body( self ):
        from Products.CMFDefault.utils import parseHeadersBody

        headers, body = parseHeadersBody( '%s\n\n%s'
                                        % ( self.COMMON_HEADERS
                                          , self.TEST_BODY
                                          )
                                        )
        self.assertEqual( len( headers ), 2 )
        self.assertEqual( body, self.TEST_BODY )

    def test_parseHeadersBody_body_malformed_terminator( self ):
        from Products.CMFDefault.utils import parseHeadersBody

        headers, body = parseHeadersBody( '%s\n \n%s'
                                        % ( self.COMMON_HEADERS
                                          , self.TEST_BODY
                                          )
                                        )
        self.assertEqual( len( headers ), 2 )
        self.assertEqual( body, self.TEST_BODY )

    def test_parseHeadersBody_preload( self ):
        from Products.CMFDefault.utils import parseHeadersBody

        preloaded = { 'Author' : 'xxx', 'text_format' : 'structured_text' }
        headers, body = parseHeadersBody( '%s\n%s\n\n%s'
                                        % ( self.COMMON_HEADERS
                                          , self.MULTILINE_DESCRIPTION
                                          , self.TEST_BODY
                                          )
                                        , preloaded
                                        )
        self.assertEqual( len( headers ), 4 )
        self.assertNotEqual( preloaded[ 'Author' ], headers[ 'Author' ] )
        self.assertEqual( preloaded[ 'text_format' ], headers[ 'text_format' ] )

    def test_scrubHTML(self):
        from Products.CMFDefault.utils import scrubHTML

        self.assertEqual( scrubHTML('<a href="foo.html">bar</a>'),
                          '<a href="foo.html">bar</a>' )
        self.assertEqual( scrubHTML('<b>bar</b>'),
                          '<b>bar</b>' )
        self.assertEqual( scrubHTML('<base href="" /><base>'),
                          '<base href="" /><base />' )
        self.assertEqual( scrubHTML('<blockquote>bar</blockquote>'),
                          '<blockquote>bar</blockquote>' )
        self.assertEqual( scrubHTML('<body bgcolor="#ffffff">bar</body>'),
                          '<body bgcolor="#ffffff">bar</body>' )
        self.assertEqual( scrubHTML('<br /><br>'),
                          '<br /><br />' )
        self.assertEqual( scrubHTML('<hr /><hr>'),
                          '<hr /><hr />' )
        self.assertEqual( scrubHTML('<img src="foo.png" /><img>'),
                          '<img src="foo.png" /><img />' )
        self.assertEqual( scrubHTML('<meta name="title" content="" /><meta>'),
                          '<meta name="title" content="" /><meta />' )

    def test_bodyfinder(self):
        from Products.CMFDefault.utils import bodyfinder

        self.assertEqual( bodyfinder(FAUX_HTML_LEADING_TEXT),
                          '\n  <h1>Not a lot here</h1>\n ' )
        self.assertEqual( bodyfinder(SIMPLE_HTML),
                          '\n  <h1>Not a lot here</h1>\n ' )
        self.assertEqual( bodyfinder(SIMPLE_STRUCTUREDTEXT),
                          SIMPLE_STRUCTUREDTEXT )
        self.assertEqual( bodyfinder(SIMPLE_XHTML),
                          '\n  <h1>Not a lot here</h1>\n ' )
        self.assertEqual( bodyfinder(STX_WITH_HTML),
                          '<p>Hello world, I am Bruce.</p>' )

    def test_html_headcheck(self):
        from Products.CMFDefault.utils import html_headcheck

        self.assertEqual( html_headcheck(FAUX_HTML_LEADING_TEXT), 0 )
        self.assertEqual( html_headcheck(SIMPLE_HTML), 1 )
        self.assertEqual( html_headcheck(SIMPLE_STRUCTUREDTEXT), 0 )
        self.assertEqual( html_headcheck(SIMPLE_XHTML), 1 )
        self.assertEqual( html_headcheck(STX_WITH_HTML), 0 )

    def test_tuplize(self):
        from Products.CMFDefault.utils import comma_split
        from Products.CMFDefault.utils import tuplize
        wanted = ('one','two','three')

        self.assertEqual( tuplize('string', 'one two three'), wanted )
        self.assertEqual( tuplize('unicode', u'one two three'), wanted )
        self.assertEqual( tuplize('string', 'one,two,three', comma_split),
                          wanted )
        self.assertEqual( tuplize('list', ['one',' two','three ']), wanted )
        self.assertEqual( tuplize('tuple', ('one','two','three')), wanted )

    def test_seq_strip(self):
        from Products.CMFDefault.utils import seq_strip

        self.assertEqual( seq_strip(['one ', ' two', ' three ']),
                          ['one','two','three'] )
        self.assertEqual( seq_strip(('one ', ' two', ' three ')),
                          ('one','two','three') )

    def test_html_marshal(self):
        from Products.CMFDefault.utils import html_marshal

        self.assertEqual( html_marshal(foo=1), ( ('foo:int', '1'), ) )
        self.assertEqual( html_marshal(foo=1, bar='baz >&baz'),
                          ( ('foo:int', '1'), ('bar', 'baz &gt;&amp;baz') ) )

    def test_toUnicode(self):
        from Products.CMFDefault.utils import toUnicode

        self.assertEqual( toUnicode('foo'), u'foo' )
        self.assertEqual( toUnicode( ('foo', 'bar'), 'ascii' ),
                          (u'foo', u'bar') )
        self.assertEqual( toUnicode( {'foo': 'bar'}, 'iso-8859-1' ),
                          {'foo': u'bar'} )

    def test_formatRFC822Headers_simple(self):
        from Products.CMFDefault.utils import formatRFC822Headers

        HEADERS = [ ('Foo', 'foo')
                  , ('Bar', 'bar')
                  ]

        formatted = formatRFC822Headers( HEADERS )

        self.assertEqual( formatted, 'Foo: foo\r\nBar: bar' )

    def test_formatRFC822Headers_empty(self):
        from Products.CMFDefault.utils import formatRFC822Headers

        HEADERS = [ ('Foo', 'foo')
                  , ('Bar', '')
                  ]

        formatted = formatRFC822Headers( HEADERS )

        self.assertEqual( formatted, 'Foo: foo\r\nBar: ' )

    def test_formatRFC822Headers_multiline(self):
        from Products.CMFDefault.utils import formatRFC822Headers

        HEADERS = [ ('Foo', 'foo')
                  , ('Bar', 'bar\nwith multiline')
                  ]

        formatted = formatRFC822Headers( HEADERS )

        self.assertEqual( formatted
                        , 'Foo: foo\r\nBar: bar\r\n  with multiline' )

    def test_formatRFC822Headers_multiline_trailing_blank_line(self):
        from Products.CMFDefault.utils import formatRFC822Headers

        HEADERS = [ ('Foo', 'foo')
                  , ('Bar', 'bar\nwith multiline\n')
                  ]

        formatted = formatRFC822Headers( HEADERS )

        self.assertEqual( formatted
                        , 'Foo: foo\r\nBar: bar\r\n  with multiline' )

    def test_formatRFC822Headers_multiline_intermediate_blank_line(self):
        from Products.CMFDefault.utils import formatRFC822Headers

        HEADERS = [ ('Foo', 'foo')
                  , ('Bar', 'bar\n\nwith multiline')
                  ]

        formatted = formatRFC822Headers( HEADERS )

        self.assertEqual( formatted
                        , 'Foo: foo\r\nBar: bar\r\n  \r\n  with multiline' )

def test_suite():
    return makeSuite(DefaultUtilsTests)

if __name__ == '__main__':
    main(defaultTest='test_suite')
