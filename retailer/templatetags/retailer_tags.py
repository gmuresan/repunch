from django.template import Library
from django import template

register = Library()

class UrlNode(template.Node):
    def __init__(self, path=None):
        self.path = path

    def render(self, context):
        request = context['request']

        return request.build_absolute_uri(self.path)

@register.tag
def absolute_url(parser, token):
    """
    returns an absolute url to this page, or optionally pass a path

    Syntax::
        {% absolute_url [path] %}
    """

    path = None

    bits = token.split_contents()
    if len(bits) >= 2:
        path = bits[1]

    return UrlNode(path)


@register.filter
def get_range( value ):
  """
    Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
      <li>0. Do something</li>
      <li>1. Do something</li>
      <li>2. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
  """
  return range( value )
