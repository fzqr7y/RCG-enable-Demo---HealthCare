# SC
# https://djangosnippets.org/snippets/9/
from django import template
from django.utils.translation import gettext_lazy as _
import re
# SC: https://snakeycode.wordpress.com/2014/10/26/django-template-filter-for-formating-currency/
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()


class ExprNode(template.Node):
    def __init__(self, expr_string, var_name):
        self.expr_string = expr_string
        self.var_name = var_name

    def render(self, context):
        try:
            clist = list(context)
            clist.reverse()
            d = {}
            d['_'] = _
            for c in clist:
                d.update(c)
            if self.var_name:
                context[self.var_name] = eval(self.expr_string, d)
                return ''
            else:
                return str(eval(self.expr_string, d))
        except:
            raise

r_expr = re.compile(r'(.*?)\s+as\s+(\w+)', re.DOTALL)


def do_expr(parser, token):
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        # raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents[0]
        raise
    m = r_expr.search(arg)
    if m:
        expr_string, var_name = m.groups()
    else:
        if not arg:
            # raise template.TemplateSyntaxError, "%r tag at least require one argument" % tag_name
            raise

        expr_string, var_name = arg, None
    return ExprNode(expr_string, var_name)
do_expr = register.tag('expr', do_expr)


@register.filter
def prepend_dollars(dollars):
    if dollars:
        dollars = round(float(dollars), 2)
        return "$%s%s" % (intcomma(int(dollars)), ("%0.2f" % dollars)[-3:])
    else:
        return ''


@register.filter
def prepend_whole_dollars(dollars):
    if dollars:
        dollars = round(float(dollars), 2)
        return "$%s" % (intcomma(int(dollars)))
    else:
        return ''
