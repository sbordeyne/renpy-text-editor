from pygments.formatter import Formatter

class TkFormatter(Formatter):
    def format(self, tokensource, outfile):
        for ttype, value in tokensource:
            outfile.write(value)
