import gi

gi.require_version('Gtk', '4.0')
from gi.repository import GLib, Gtk


class SearchBarApp(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="GTK4 Search Bar Example")
        self.set_default_size(600, 400)
        
        # Create main container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_child(main_box)
        
        # Create header bar
        header_bar = Gtk.HeaderBar()
        self.set_titlebar(header_bar)
        
        # Create search button for header bar
        search_button = Gtk.ToggleButton()
        search_button.set_icon_name("system-search-symbolic")
        search_button.connect("toggled", self.on_search_toggled)
        header_bar.pack_start(search_button)
        
        # Create search bar
        self.search_bar = Gtk.SearchBar()
        main_box.append(self.search_bar)
        
        # Create search entry
        self.search_entry = Gtk.SearchEntry()
        self.search_entry.connect("search-changed", self.on_search_changed)
        self.search_entry.connect("stop-search", self.on_stop_search)
        self.search_bar.set_child(self.search_entry)
        
        # Connect search bar to search button
        self.search_bar.connect_entry(self.search_entry)
        
        # Create scrolled window for content
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        main_box.append(scrolled)
        
        # Create list view with sample data
        self.setup_list_view(scrolled)
        
        # Store original data for filtering
        self.original_data = [
            "Apple", "Banana", "Cherry", "Date", "Elderberry",
            "Fig", "Grape", "Honeydew", "Kiwi", "Lemon",
            "Mango", "Orange", "Papaya", "Quince", "Raspberry"
        ]
        self.update_list(self.original_data)
        
        # Set up keyboard shortcuts
        self.setup_shortcuts()
    
    def setup_list_view(self, parent):
        # Create list store
        self.list_store = Gtk.StringList()
        
        # Create list view
        self.list_view = Gtk.ListView()
        
        # Create selection model
        selection_model = Gtk.SingleSelection(model=self.list_store)
        self.list_view.set_model(selection_model)
        
        # Create factory for list items
        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", self.on_factory_setup)
        factory.connect("bind", self.on_factory_bind)
        self.list_view.set_factory(factory)
        
        parent.set_child(self.list_view)
    
    def on_factory_setup(self, factory, list_item):
        label = Gtk.Label()
        label.set_xalign(0)
        list_item.set_child(label)
    
    def on_factory_bind(self, factory, list_item):
        label = list_item.get_child()
        string_object = list_item.get_item()
        label.set_text(string_object.get_string())
    
    def update_list(self, items):
        # Clear existing items
        self.list_store.splice(0, self.list_store.get_n_items(), [])
        
        # Add new items
        for item in items:
            self.list_store.append(item)
    
    def setup_shortcuts(self):
        # Create shortcut controller
        controller = Gtk.ShortcutController()
        
        # Add Ctrl+F shortcut
        shortcut = Gtk.Shortcut()
        shortcut.set_trigger(Gtk.ShortcutTrigger.parse_string("<Control>f"))
        shortcut.set_action(Gtk.CallbackAction.new(self.activate_search))
        controller.add_shortcut(shortcut)
        
        # Add Escape shortcut
        escape_shortcut = Gtk.Shortcut()
        escape_shortcut.set_trigger(Gtk.ShortcutTrigger.parse_string("Escape"))
        escape_shortcut.set_action(Gtk.CallbackAction.new(self.deactivate_search))
        controller.add_shortcut(escape_shortcut)
        
        self.add_controller(controller)
    
    def activate_search(self, widget, args):
        self.search_bar.set_search_mode(True)
        return True
    
    def deactivate_search(self, widget, args):
        if self.search_bar.get_search_mode():
            self.search_bar.set_search_mode(False)
            return True
        return False
    
    def on_search_toggled(self, button):
        # Toggle search bar visibility
        is_active = button.get_active()
        self.search_bar.set_search_mode(is_active)
        
        if is_active:
            self.search_entry.grab_focus()
    
    def on_search_changed(self, search_entry):
        search_text = search_entry.get_text().lower()
        
        if not search_text:
            # Show all items if search is empty
            filtered_data = self.original_data
        else:
            # Filter items based on search text
            filtered_data = [
                item for item in self.original_data 
                if search_text in item.lower()
            ]
        
        self.update_list(filtered_data)
    
    def on_stop_search(self, search_entry):
        # Clear search and hide search bar
        search_entry.set_text("")
        self.search_bar.set_search_mode(False)

class SearchBarApplication(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.example.searchbar")
    
    def do_activate(self):
        window = SearchBarApp(self)
        window.present()

if __name__ == "__main__":
    app = SearchBarApplication()
    app.run()import emoji

# Get all emojis as a dictionary
all_emojis = emoji.EMOJI_DATA

# Or get just the emoji characters
emoji_list = list(emoji.EMOJI_DATA.keys())

# You can also get emojis by category
for emoji_char, data in emoji.EMOJI_DATA.items():
    print(f"{emoji_char}: {data['en']} (Category: {data.get('status', 'unknown')})")
