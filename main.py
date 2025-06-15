def main():
    import emoji
    import gi

    all_emoji = emoji.EMOJI_DATA
    # all_emoji = dict(
    #    zip([str(x) for x in range(1, 65)], [str(x) for x in range(1, 65)])
    # )
    print(len(all_emoji))

    gi.require_version("Gtk", "4.0")
    from gi.repository import Gdk, Gtk, Pango

    clipboard = Gdk.Display.get_default().get_clipboard()

    class EmojiButton(Gtk.Button):
        def __init__(self, emoji: str = ""):
            super().__init__()

            self.emoji = emoji

            label = Gtk.Label()
            label.set_markup(f"<big>{emoji}</big>")

            self.set_child(label)

            self.props.margin_top = self.props.margin_bottom = (
                self.props.margin_start
            ) = self.props.margin_end = 0

            self.props.has_frame = False

            self.connect("clicked", self.on_click)

        def on_click(self, _widget):
            clipboard.set(f"{self.emoji}")

    class MyWindow(Gtk.ApplicationWindow):
        def __init__(self, **kargs):
            # inherit window properties and set window title
            super().__init__(**kargs, title="pmoji")

            # self.set_default_size(200, 80)
            # self.set_decorated(False)

            self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

            self.top_box = Gtk.Box()
            self.search_bar = Gtk.SearchBar()

            self.search_entry = Gtk.SearchEntry()
            self.search_bar.connect_entry(self.search_entry)
            self.search_entry.props.hexpand = True

            self.search_bar.set_child(self.search_entry)
            self.search_bar.set_search_mode(True)

            self.exit_button = Gtk.Button(has_frame=False)
            self.exit_button.connect("clicked", self.close_window)

            self.scrollable_window = Gtk.ScrolledWindow()
            self.scrollable_window.props.propagate_natural_width = True
            self.scrollable_window.props.vexpand = True

            self.set_default_size(self.get_default_size()[0], 300)
            self.props.resizable = False

            self.flowbox = Gtk.FlowBox()
            self.flowbox.set_max_children_per_line(8)

            for emoji in all_emoji.keys():
                self.flowbox.append(EmojiButton(emoji))

            self.scrollable_window.set_child(self.flowbox)

            self.top_box.append(self.search_bar)
            self.top_box.append(self.exit_button)

            self.main_box.append(self.top_box)
            self.main_box.append(self.scrollable_window)
            self.set_child(self.main_box)

            self.flowbox.grab_focus()

        def close_window(self, _widget):
            self.close()

    def on_activate(app):
        win = MyWindow(application=app)
        win.present()

    app = Gtk.Application(application_id="nyx.zack.pmoji")
    app.connect("activate", on_activate)

    app.run()


if __name__ == "__main__":
    main()
