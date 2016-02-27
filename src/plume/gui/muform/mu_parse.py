from .mu_base import *
    # Last Error Code: 30229

class MuParse():
    # Class to parse html for <( )> tags
    # Last Error Code: 30201
    def __init__(self):
        self.b_debug = False

    def __replace_white(self, s_value):
        # Returns s_value with \n and double spaces replaced by a single space
        s_value = s_value.replace('\n', ' ')
        while s_value.find('  ') != -1:
            s_value = s_value.replace('  ', ' ')

        return s_value.strip()

    def __debug(self, s_state, s_value):
        if self.b_debug:
            print(s_state + '=' + self.__replace_white(s_value)[:80])

    def __debug_tag(self, s_state, a_tag):
        # Output tag tuple
        if self.b_debug:
            if not isinstance(a_tag, tuple):
                try:
                    print('Expected tuple, found: ' + type(a_tag).__name__)
                except:
                    print('Expected tuple, found unknown type')
                return

            s_pre = a_tag[1]
            if s_pre:
                s_pre = self.__replace_white(s_pre[:20])

            s_post = a_tag[2]
            if s_post:
                s_post = self.__replace_white(s_post[:20])

            print(s_state + ': tag=|' + a_tag[0] + '|')
            print('  pre:|' + s_pre + '|')
            print('  post:|' + s_post + '|')

    def __debug_func(self, s_state, a_func):
        # Output tag tuple
        if self.b_debug:
            if not isinstance(a_func, tuple):
                try:
                    print('Expected tuple, found: ' + type(a_func).__name__)
                except:
                    print('Expected tuple, found unknown type')
                return

            print(s_state + ': func=|' + a_func[0] + '|')
            a_args = a_func[1]
            if not isinstance(a_args, tuple):
                try:
                    print('Expected tuple, found: ' + type(a_args).__name__)
                except:
                    print('Expected tuple, found unknown type')
                return

            for i, a_arg in a_args:
                print('  ' + str(i) + '=' + a_arg)

    def __debug_print(self, s_state, a_tuple):
        if self.b_debug:
            if not isinstance(a_tuple, tuple):
                try:
                    print('Expected tuple, found: ' + type(a_tuple).__name__)
                except:
                    print('Expected tuple, found unknown type')
                return

            print(s_state)
            print(a_tuple)

    def __func_name(self, s_stream, s_tag):
        # Returns the func name. No quotes allowed. s_stream is the remainder of the unparsed text (i.e. initially
        # the same as s_tag). s_tag is passed to give context to any errors.
        s_ret = ''
        for p, c in enumerate(s_stream):
            # Ignore whitespace
            if c.isspace():
                continue
            # Wait for comma
            if c == ',':
                a_ret = (s_ret, s_stream[p+1:], s_tag)
                return a_ret
            else:
                # Only a-z0-9_- allowed
                if "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_".find(c) == -1:
                    base_error(30221, 'Function name can only be A-Z0-9_- (and no quotes) Tag: ' + s_tag)
                    a_ret = ('', ())    # Empty func + args
                    return a_ret
                s_ret += c
        # Get here if no comma (end of func, no args)
        a_ret = (s_ret, '', s_tag)
        return a_ret


    def __get_arg_nq(self, s_stream, s_tag):
        # Get arg without quotes
        s_ret = ''
        for p, c in enumerate(s_stream):
            # Ignore white space
            if c.isspace():
                continue
            # Look for quotes
            if c == '"' or c == "'":
                # Not allowed quotes in the middle of an arg
                base_error(30222, 'Illegal quote: (' + c + ') Tag: ' + s_tag)
                a_ret = ('', ())    # Empty func + args
                return a_ret
            if c == ',':
                # end of arg
                a_ret = (s_ret, s_stream[p+1:], s_tag)
                return a_ret

            # Else it's part of the arg
            s_ret += c
        # Get here if no more chars
        a_ret = (s_ret, '', s_tag)
        return a_ret

    def __comma_or_end(self, s_stream, s_tag):
        # Expects a comma or end of stream. Return (','...) if the stream is valid. (''...) implies a missing comma
        for p, c in enumerate(s_stream):
            # Ignore whitespace
            if c.isspace():
                continue
            if c == ',':
                # Comma found, remove it from stream
                a_ret = (',', s_stream[p+1:], s_tag)
                return a_ret
            else:
                # Else no comma
                if s_stream:
                    # If we didn't find a comma, there can be no more arguments
                    base_error(30225, 'Missing comma (,) before: "' + s_stream[:20] + '" Tag: ' + s_tag)
                    a_ret = ('', ())    # Empty func + args
                    return a_ret
                # Else return empty stream
                a_ret = (',', '', s_tag)
                return a_ret

        # stream was empty on entry
        a_ret = (',', '', s_tag)
        return a_ret

    def __get_arg_sq(self, s_stream, s_tag):
        # Get single quoted arg (returned without quotes). Initial quote has already been removed
        s_ret = ''
        for p, c in enumerate(s_stream):
            # Look for closing quote
            if c == "'":
                # end of arg, remove any comma
                a_ret = self.__comma_or_end(s_stream[p+1:], s_tag)
                # a_ret[0] is ',' if the stream was valid (does not imply a comma exists!)
                if not a_ret[0]:
                    # Comma missing. Error already given
                    a_ret = ('', ())
                    return a_ret

                s_stream = a_ret[1]
                a_ret = (s_ret, s_stream, s_tag)
                return a_ret
            else:
                # Inside quotes, all chars count, including whitespace, but not the quote
                s_ret += c

        # Get here if no closing quote
        base_error(30223, "Missing closing quote (').  Tag: " + s_tag)
        a_ret = ('', ())    # Empty func + args
        return a_ret

    def __get_arg_dq(self, s_stream, s_tag):
        # Get double quoted arg (returned without quotes). Initial quote has already been removed
        s_ret = ''
        for p, c in enumerate(s_stream):
            # Look for closing quote
            if c == '"':
                # end of arg, remove any comma
                a_ret = self.__comma_or_end(s_stream[p+1:], s_tag)
                # a_ret[0] is ',' if the stream was valid (does not imply a comma exists!)
                if not a_ret[0]:
                    # Comma missing. Error already given
                    a_ret = ('', ())
                    return a_ret
                s_stream = a_ret[1]
                a_ret = (s_ret, s_stream, s_tag)
                return a_ret
            else:
                # Inside quotes, all chars count, including whitespace, but not the quote
                s_ret += c

        # Get here if no closing quote
        base_error(30224, 'Missing closing quote (").  Tag: ' + s_tag)
        a_ret = ('', ())    # Empty func + args
        return a_ret

    def __get_arg(self, s_stream, s_tag):
        # Arg dispatcher, no quotes, single quotes or double quotes
        # Ignore white space
        for p, c in enumerate(s_stream):
            if c.isspace():
                continue
            # Look for quotes
            if c == '"' :
                # Dbl quotes
                return self.__get_arg_dq(s_stream[p+1:], s_tag)
            elif c == "'":
                # Single quotes
                return self.__get_arg_sq(s_stream[p+1:], s_tag)
            else:
                # Not quoted
                return self.__get_arg_nq(s_stream[p:], s_tag)

    def get_tag(self, s_html):
        # Given a string of html with embedded tags of the form <(tag)>,
        # returns a tuple consisting of 3 strings: ('<(tag)>', 'pre_html', 'post_html')
        # If no tag, returns ('', s_html, '')
        # Examples: if input is '0123<(abcd)>4567' then returns ('<(abcd)>', '0123', '4567')
        self.__debug('get_tag', s_html)

        p = s_html.find('<(')
        if p == -1:
            # No more tags
            self.__debug('no more tags', s_html)
            a_ret = ('', s_html, '')
            return a_ret

        # Find close tag AFTER start
        q = s_html.find(')>', p)
        if q == -1:
            # No closing tag. Treat it like no tag
            base_error(30226, 'No closing tag after ' + s_html[p:30])
            a_ret = ('', s_html, '')
            return a_ret

        a_ret = (s_html[p:q+2], s_html[:p], s_html[q+2:])
        self.__debug_tag('return tag', a_ret)
        return a_ret

    def unpack_tag(self, s_tag):
        # Given a tag of the form <(func_name ,arg1, ... ,argn)>,
        # returns a tuple consisting of: the function name and a tuple of args e.g: (tag, (arg1, ... argn))
        # If there are no args, then the inner tuple is empty ()
        # Note: function name must be unquoted. Args are either quoted or unquoted. All are comma separated.
        self.__debug('unpack_tag', s_tag)

        # [2:-2] to remove tag marks "<()>"
        a_ret = self.__func_name(s_tag[2:-2], s_tag)
        s_func = a_ret[0] # function name
        s_stream = a_ret[1]

        if not s_func:
            # Empty function name is an error (already output)
            base_error(30227, 'No function name. Tag: ' + s_tag)
            a_ret = ('', ())    # Empty func + args
            return a_ret

        self.__debug('unpack_tag', s_tag)
        #print (s_func, s_stream)

        a_args = []         # Args list to return (as tuple)
        while s_stream:
            a_ret = self.__get_arg(s_stream, s_tag)
            a_args.append(a_ret[0])
            s_stream = a_ret[1]

        # Return (func_name, (arg1, arg2, argn))
        a_ret = (s_func, tuple(a_args))
        #self.__debug_func('return ', a_ret)

        return a_ret

    def parse_html(self, a_caller, s_html):
        # Replaces tags in s_html with callback to a_caller
        a_ret = self.get_tag(s_html)
        s_tag = a_ret[0]
        s_pre_html = a_ret[1]
        s_post_html = a_ret[2]
        while s_tag:
            # We found a tag, process it
            if s_tag[2:].strip()[:1] == '#':
                # This is a comment
                s_result = ''
            else:
                a_tag = self.unpack_tag(s_tag)
                s_func_name = a_tag[0]
                a_args = a_tag[1]
                if not s_func_name:
                    # The parse failed. We have already given an error. Add something to the html to make it easier to debug
                    s_result = 'Error 30302'
                    base_error(30302, 'Parse failed. Error already given')
                else:
                    # We add mfn_ to the function name to prevent accidental calling of unexpected methods
                    s_func_name = 'mfn_' + s_func_name
                    # Call the function
                    self.__debug_print('Calling: ' + s_func_name + ' Args: ', a_args)
                    if hasattr(a_caller, s_func_name):
                        s_result = getattr(a_caller, s_func_name)(*a_args)
                        #s_result = '###'
                    else:
                        # No callback function of that name
                        s_result = '[Error 30229]'

            # Now re-combine html and re-parse
            s_html = s_pre_html + s_result + s_post_html

            a_ret = self.get_tag(s_html)
            s_tag = a_ret[0]
            s_pre_html = a_ret[1]
            s_post_html = a_ret[2]

        # s_pre_html is the final result
        return s_html

