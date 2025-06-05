def main():
    import gi

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
            ) = self.props.margin_end = 15

            self.connect("clicked", self.on_click)

        def on_click(self, _widget):
            clipboard.set(f"{self.emoji}")

    class MyWindow(Gtk.ApplicationWindow):
        def __init__(self, **kargs):
            # inherit window properties and set window title
            super().__init__(**kargs, title="pmoji")

            self.set_default_size(200, 80)

            self.props.show_menubar = (
                True  # This is needed since the menubar hides by default
            )

            box = Gtk.Box(spacing=0, homogeneous=True)
            self.set_child(box)

            button1 = EmojiButton("💔")
            box.append(button1)

            button2 = EmojiButton("🥀")
            box.append(button2)

    def on_activate(app):
        win = MyWindow(application=app)
        win.present()

    app = Gtk.Application(application_id="nyx.zack.pmoji")
    app.connect("activate", on_activate)

    app.run()


if __name__ == "__main__":
    main()
