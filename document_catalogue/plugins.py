"""
Dependency Injection Micro-Framework using Plugins

    A Plugin provides some custom behaviour to specific Concrete classes in the class hierarchy
    The Base class of the hierarchy generally applies the plugins by adding PluginManager as a mixin
    Plugins can then be injected into any concrete class in its hierarchy.

"""

from abc import ABCMeta
from itertools import chain
from django.db.models.functions import Lower

#########################
#  Abstract Base Classes - plugin architecture
#########################


class PluginManager:
    """
        A simple, generic plugin manager.
        Provides a clean dependency injection mechanism when used as a Mixin: BaseClass(PluginManager)
        BaseClass implements behaviours for plugins (defined by whatever interface suited to app)
        ConcreteSubclass(BaseClass) can then RegisterPlugins to inject additional behaviours
    """
    plugins = []

    @classmethod
    def add_plugins(cls, plugins):
        cls.plugins = list(chain(cls.plugins, plugins))

    @classmethod
    def apply_plugins(cls, f):
        """ Apply f to each plugin.  f must be a callable that takes a single plugin parameter """
        for plugin in cls.plugins :
            try:
                f(plugin)
            except AttributeError:
                pass


class RegisterPlugins :
    """
        A Decorator for registering a set of plugins to a PluginManager
        E.g.:  @RegisterPlugins(Plugin1(some, parameters), Plugin2())
    """
    def __init__(self, *plugins) :
        self.plugins = plugins

    def __call__(self, decorated_class) :
        decorated_class.add_plugins(self.plugins)

        return decorated_class


#########################
#  Concrete Implementations - document_catalogue plugins
#########################


class ViewPluginManager(PluginManager):
    """ Encapsulates logic specific to applying AbstractViewPlugin plugins.  Intended as View mixin """
    @classmethod
    def plugins_extend_qs(cls, request, qs):
        """ Apply each plugin to the given queryset, in sequence, return resulting queryset """
        for plugin in cls.plugins :
            try:
                qs = plugin.extend_qs(request, qs)
            except AttributeError:
                pass
        return qs

    @classmethod
    def plugins_get_context(cls, request):
        context = {}
        cls.apply_plugins(lambda plugin: context.update(plugin.get_context(request)))
        return context


class AbstractViewPlugin(metaclass=ABCMeta):
    """ Defines the API for a plugin that injects behaviour into a View class """
    def apply(self, request):
        """ Apply the plugin to the given request just prior to dispatching it """
        pass

    def extend_qs(self, request, qs):
        """ Extend, modify, or constrain the base document queryset and return it """
        return qs

    def get_context(self, request):
        """ Return a dictionary to be added to the View's context """
        return {}


class OrderedViewPlugin(AbstractViewPlugin):
    """ Applies ordering to view's queryset based on URL query argument found in request.GET """
    ORDERING_CHOICES = (
        ('default', 'Default'),
        ('date', 'Recently Updated'),
        ('title', 'Title')
    )
    ORDERING_KEYS = tuple(k for k,v in ORDERING_CHOICES)

    ORDERING_EXPRESSION = {   # valid ordering expressions maps query param value to ordering clause
        'date' : '-update_date',
        'title': Lower('title').asc(),
    }

    def __init__(self, query_param='dc_ordering'):
        """ Name of the query parameter used to specify ordering """
        super().__init__()
        self.query_param = query_param

    def get_ordering_key(self, request):
        key = request.GET.get(self.query_param, None)
        return key if key in self.ORDERING_KEYS else None

    def get_ordering(self, request):
        """ Return the order_by experession for the queryset """
        return self.ORDERING_EXPRESSION.get(self.get_ordering_key(request), None)

    def extend_qs(self, request, qs):
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(ordering)
        return qs

    def get_context(self, request):
        return {
            self.query_param : self.get_ordering_key(request),
            '{ordering}_choices'.format(ordering=self.query_param) : self.ORDERING_CHOICES,
        }


class SessionOrderedViewPlugin(OrderedViewPlugin):
    """ Applies ordering to view's queryset based on ordering passed in URL query arg and stored in session """

    def get_ordering_key(self, request):
        key = request.session.get(self.query_param, None)
        return key if key in self.ORDERING_KEYS else None

    def apply(self, request):
        """ Apply the plugin to the given request """
        ordering_key = super().get_ordering_key(request)
        if ordering_key:
            request.session[self.query_param] = ordering_key
