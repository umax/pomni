#
# component.py <Peter.Bienstman@UGent.be>
#


class Component(object):

    """Base class of components that are registered with the component
    manager. This is a list of component types: config, log, database,
    scheduler, stopwatch, translator, filter, card_type, card_type_converter,
    card_type_widget, generic_card_type_widget, ui_component, renderer,
    controller, main_widget, review_controller, review_widget, file format,
    plugin, hook, activity_criterion, criterion_applier, statistics_page,
    all the abstract dialogs, ...      

    'used_for' can store certain relationships between components, e.g.
    a card type widget is used for a certain card type.

    Most of the time, instances are stored here, apart from widgets when
    classes are stored. (Instantiating a complex widget can take a lot of
    time on a mobile device, and should be done lazily.) Only the main
    widget is stored as an instance here.

    When 'instantiate == LATER', the component is lazily created when needed.
    The instance is not cached for subsequent reuse, as these widgets
    typically can become obsolete/overwritten by plugins.

    Each component has access to all of the context of the other components
    because it hold a reference to the user's component manager.

    We need to pass the context of the component manager already in the
    constructor, as many component make use of it in their __init__ method.
    This means that derived components should always call the
    Component.__init__ if they provide their own constructor.
    
    """
    
    component_type = ""
    used_for = None

    IMMEDIATELY = 0
    LATER = 1
    
    instantiate = IMMEDIATELY
    
    def __init__(self, component_manager):
        self.component_manager = component_manager

    def activate(self):

        """Initialisation code called when the component is about to do actual
        work, and which can't happen in the constructor, e.g. because
        components on which it relies have not yet been registered.

        """

        pass

    def deactivate(self):        
        pass

    # Convenience functions, for easier access to all of the context of
    # libmnemosyne from within a component.
    
    def _(self):
        return self.component_manager.get_current("translator")
    
    def config(self):
        return self.component_manager.get_current("config")

    def log(self):
        return self.component_manager.get_current("log")

    def database(self):
        return self.component_manager.get_current("database")

    def scheduler(self):
        return self.component_manager.get_current("scheduler")
    
    def stopwatch(self):
        return self.component_manager.get_current("stopwatch")
    
    def main_widget(self):
        return self.component_manager.get_current("main_widget")

    def controller(self):
        return self.component_manager.get_current("controller")

    def review_controller(self):
        return self.component_manager.get_current("review_controller")

    def card_types(self):
        return self.component_manager.get_all("card_type")

    def filters(self):
        return self.component_manager.get_all("filter")

    def plugins(self):
        return self.component_manager.get_all("plugin")

    def statistics_pages(self):
        return self.component_manager.get_all("statistics_page")
    
    def configuration_widgets(self):
        return self.component_manager.get_all("configuration_widget")
    
    def card_type_by_id(self, id):
        return self.component_manager.card_type_by_id[id]
