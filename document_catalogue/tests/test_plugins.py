from django.test import TestCase
from document_catalogue import plugins

class FrameworkTests(TestCase):
    """
        Test basic behaviours for Plugin Micro-Framework
    """
    class TestPluginManager(plugins.PluginManager):
        def __init__(self):
            self.counter = 0

        def count(self):
            self.counter += 1

    def test_plugin_manager(self):
        class Subclass(self.TestPluginManager):
            pass

        t = Subclass()
        plugins = ('a', 'b', 'c')
        t.add_plugins(plugins)
        self.assertEqual(t.plugins, list(plugins))

        t.apply_plugins(lambda plugin: t.count())
        self.assertEqual(t.counter, len(plugins))

    def test_plugin_manager_inheritance(self):
        class Subclass1(self.TestPluginManager):
            pass
        class Subclass2(self.TestPluginManager):
            pass
        class SubSubclass(Subclass1):
            pass

        t = Subclass1()
        plugins = ('a', 'b', 'c')
        t.add_plugins(plugins)

        s = Subclass2()
        more_plugins = ('d', 'e')
        s.add_plugins(more_plugins)

        s.apply_plugins(lambda plugin: s.count())
        self.assertEqual(s.counter, len(more_plugins))

        r = SubSubclass()
        r.add_plugins(more_plugins)
        self.assertEqual(set(t.plugins), set(plugins))
        self.assertEqual(set(s.plugins), set(more_plugins))
        self.assertEqual(set(r.plugins), set(plugins) | set(more_plugins))

        r.apply_plugins(lambda plugin: r.count())
        self.assertEqual(r.counter, len(plugins) + len(more_plugins))


    def test_register_plugins(self):
        @plugins.RegisterPlugins('w', 'x', 'y', 'z')
        class Subclass(self.TestPluginManager):
            pass

        s = Subclass()
        s.apply_plugins(lambda plugin: s.count())
        self.assertEqual(s.counter, 4)  # one for each plugin added above


class ViewPluginTests(TestCase):
    """
        Test behaviours for View Plugins
    """
    class TestViewPluginManager(plugins.ViewPluginManager):
        pass

    class TestViewPlugin(plugins.AbstractViewPlugin):
        def apply(self, request):
            request.count += 1

        def extend_qs(self, request, qs):
            return qs + 10

        def get_context(self, request):
            return {'plugin_context': 'Some Value'}

    def setUp(self):
        @plugins.RegisterPlugins(self.TestViewPlugin(), self.TestViewPlugin())
        class Subclass(self.TestViewPluginManager):
            pass

        self.plugin_manager = Subclass()

    def test_apply_plugins(self):
        request = lambda : None
        request.count = 0
        self.plugin_manager.apply_plugins(lambda plugin: plugin.apply(request))
        self.assertEqual(request.count, 2)

    def test_extend_qs(self):
        qs = 0
        qs = self.plugin_manager.plugins_extend_qs(None, qs)
        self.assertEqual(qs, 20)

    def test_get_context(self):
        ctx = self.plugin_manager.plugins_get_context(None)
        self.assertTrue('plugin_context' in ctx)


class OrderedViewPluginTestBase(TestCase):
    """
        Set up for OrderedView Plugin Tests
    """
    class TestViewPluginManager(plugins.ViewPluginManager):
        pass
    ORDER_KEY = 'the_order_key'
    ORDER_FIELD = 'date'
    ORDER_EXPERSSION = plugins.OrderedViewPlugin.ORDERING_EXPRESSION[ORDER_FIELD]
    PLUGIN = None

    def setUp(self):
        @plugins.RegisterPlugins(self.PLUGIN)
        class Subclass(self.TestViewPluginManager):
            pass

        self.plugin_manager = Subclass()

        self.request = lambda : None
        self.request.GET = {self.ORDER_KEY: self.ORDER_FIELD}
        self.request.session = {}

        class QS:
            def __init__(self):
                self.ordering = None
            def order_by(self, ordering):
                self.ordering = ordering
        self.qs = QS()


class OrderedViewPluginTests(OrderedViewPluginTestBase):
    """
        Test behaviours for OrderedView Plugins
    """
    PLUGIN = plugins.OrderedViewPlugin(OrderedViewPluginTestBase.ORDER_KEY)

    def test_extend_qs(self):
        qs = self.plugin_manager.plugins_extend_qs(self.request, self.qs)
        self.assertEqual(self.qs.ordering, self.ORDER_EXPERSSION)

    def test_get_context(self):
        ctx = self.plugin_manager.plugins_get_context(self.request)
        self.assertTrue(self.ORDER_KEY in ctx)
        self.assertEqual(ctx[self.ORDER_KEY], self.ORDER_FIELD)
        self.assertTrue(self.ORDER_KEY+'_choices' in ctx)


class SessionOrderedViewPluginTests(OrderedViewPluginTestBase):
    """
        Test behaviours for SessionOrderedView Plugins
    """
    PLUGIN = plugins.SessionOrderedViewPlugin(OrderedViewPluginTestBase.ORDER_KEY)

    def test_apply_plugins(self):
        self.plugin_manager.apply_plugins(lambda plugin: plugin.apply(self.request))
        self.assertEqual(self.request.session[self.ORDER_KEY], self.ORDER_FIELD)

    def test_extend_qs(self):
        self.plugin_manager.apply_plugins(lambda plugin: plugin.apply(self.request))
        qs = self.plugin_manager.plugins_extend_qs(self.request, self.qs)
        self.assertEqual(self.qs.ordering, self.ORDER_EXPERSSION)

    def test_get_context(self):
        self.plugin_manager.apply_plugins(lambda plugin: plugin.apply(self.request))
        ctx = self.plugin_manager.plugins_get_context(self.request)
        self.assertTrue(self.ORDER_KEY in ctx)
        self.assertEqual(ctx[self.ORDER_KEY], self.ORDER_FIELD)
        self.assertTrue(self.ORDER_KEY+'_choices' in ctx)
