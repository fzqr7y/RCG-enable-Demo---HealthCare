# SC
# https://djangosnippets.org/snippets/9/
from django import template
from django.utils.translation import gettext_lazy as _
import re
# SC: https://snakeycode.wordpress.com/2014/10/26/
# django-template-filter-for-formating-currency/
from django.contrib.humanize.templatetags.humanize import intcomma
# http://stackoverflow.com/questions/18364547/django-custom-filter-to-check-if-file-exists
# from django.core.files.storage import default_storage
# from django.contrib.staticfiles.storage import staticfiles_storage
# from django.contrib.staticfiles import finders
from django.contrib.auth.models import Group

# import os
# from django.conf import settings
# from django.templatetags.static import static
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

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
        # raise template.TemplateSyntaxError, "%r tag requires
        # arguments" % token.contents[0]
        raise
    m = r_expr.search(arg)
    if m:
        expr_string, var_name = m.groups()
    else:
        if not arg:
            # raise template.TemplateSyntaxError, "%r tag at
            # least require one argument" % tag_name
            raise

        expr_string, var_name = arg, None
    return ExprNode(expr_string, var_name)


do_expr = register.tag('expr', do_expr)


@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return group in user.groups.all()


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
        return '-'


@register.filter
def percentage(fraction):
    try:
        return ("%.2f" % float(fraction)).rstrip('0').rstrip('.') + "%"
    except ValueError:
        return ''


@register.filter
def decimalize(fraction):
    try:
        return ("%0.1f" % float(fraction)).rstrip('0').rstrip('.')
    except ValueError:
        return ''

# @register.filter
# def safe_avatar(filepath, malefemale):
#     # fp = filepath
#     # logger.error(static(filepath))
#     # logger.error(settings.BASE_DIR)
#     # tmp_filepath = static(filepath).strip("/")
#     # logger.error(tmp_filepath)
#     # new_filepath = os.path.join(
#     #     settings.BASE_DIR, static(filepath).strip("/"))
#     # logger.error(new_filepath)
#     # logger.error(fp)
#     # if default_storage.exists(static(filepath).strip("/")):
#     # logger.error(finders.find(filepath))
#     if (filepath and finders.find(filepath)):
#         return filepath
#     elif malefemale == 'F':
#         # new_filepath = os.path.join(
#         #     settings.BASE_DIR, static('img/avatars/female.png'))
#         new_filepath = 'img/avatars/female.png'
#         return new_filepath
#     else:
#         # index = filepath.rfind('/')
#         # new_filepath = filepath[:index] + '/image.png'
#         new_filepath = 'img/avatars/male.png'
#         return new_filepath

# app/templatetags/getattribute.py


# http://stackoverflow.com/questions/844746/performing-a-getattr-style-lookup-in-a-django-template
numeric_test = re.compile("^\d+$")


def getattribute(value, arg):
    """Gets an attribute of an object dynamically from a string name"""

    if hasattr(value, str(arg)):
        return getattr(value, arg)
    elif hasattr(value, 'has_key') and arg in value:
        return value[arg]
    elif numeric_test.match(str(arg)) and len(value) > int(arg):
        return value[int(arg)]
    else:
        return 'NA'


register.filter('getattribute', getattribute)
