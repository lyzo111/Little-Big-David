from nicegui import ui


class Tutorial:
    def __init__(self):
        """
        Initialize the Tutorial class with the current step set to 0 and predefined tutorial steps.
        """
        self.current_step = 0
        self.tutorial_steps = [
            {"title": "Willkommen bei Little Big David!",
             "description": "Little Big David ist ein Abenteuer, bei dem du Aufgaben erfüllst, um deinen Charakter zu stärken. "
                            "Erkunde die Welt, besiege Gegner und sammle Items!"},
            {"title": "Deine erste Aufgabe",
             "description": "David ist noch klein. Er braucht XP, um zu wachsen. Erfülle tägliche Aufgaben wie '10 Minuten meditieren' oder 'einen Spaziergang machen', um stärker zu werden."},
            {"title": "Kämpfe und Buffs",
             "description": "David kann Gegner besiegen, um Buffs zu erhalten, oder alternative Wege gehen, um Items zu sammeln. "
                            "Das Ziel ist, stark genug zu werden, um die Endgegner zu besiegen!"},
            {"title": "Retirement-System",
             "description": "Wenn David stark genug ist, kann er sich zur Ruhe setzen. Aber Vorsicht: Nach dem Retirement werden seine Stats zurückgesetzt. "
                            "Er erhält jedoch Belohnungen wie neue Fähigkeiten oder seltene Ausrüstung!"},
            {"title": "Haupt- und Nebenquests",
             "description": "Absolviere Hauptquests, um die Geschichte voranzutreiben, oder erkunde die Welt für Nebenquests, um Schätze und Buffs zu finden."},
            {"title": "Fertig!",
             "description": "Jetzt bist du bereit, David auf sein Abenteuer zu schicken! Viel Spaß beim Spielen von Little Big David."}
        ]

    def next_step(self):
        """
        Move to the next step in the tutorial if not already at the last step.
        """
        if self.current_step < len(self.tutorial_steps) - 1:
            self.current_step += 1
            self.update_ui()

    def previous_step(self):
        """
        Move to the previous step in the tutorial if not already at the first step.
        """
        if self.current_step > 0:
            self.current_step -= 1
            self.update_ui()

    def skip_tutorial(self):
        """
        Display a dialog to confirm if the user wants to skip the tutorial.
        """
        with ui.dialog() as dialog:
            with ui.card():
                ui.label("Tutorial wirklich überspringen?")
                with ui.row().classes("justify-around mt-4"):
                    ui.button("Ja", on_click=lambda: self.end_tutorial(dialog))
                    ui.button("Nein", on_click=dialog.close)

    def end_tutorial(self, dialog):
        """
        End the tutorial, close the dialog, and clear the tutorial UI.
        """
        dialog.close()
        ui.notify("Tutorial beendet!")
        self.tutorial_ui.clear()
        with self.tutorial_ui:
            ui.label("Willkommen in Little Big David! Viel Spaß beim Spielen!").classes("text-xl font-bold mt-10")

    def update_ui(self):
        """
        Update the UI elements to reflect the current step in the tutorial.
        """
        step = self.tutorial_steps[self.current_step]
        self.title.content = step["title"]
        self.description.content = step["description"]
        self.progress_bar.value = (self.current_step + 1) / len(self.tutorial_steps)

    def show(self):
        """
        Display the tutorial UI with navigation buttons and progress bar.
        """
        with ui.column().classes("items-center justify-center") as self.tutorial_ui:
            with ui.card().classes("w-1/2"):
                self.title = ui.label().classes("text-xl font-bold mb-4")
                self.description = ui.label().classes("mb-4")
                self.progress_bar = ui.progress().classes("w-full mb-4")

                with ui.row().classes("justify-around"):
                    ui.button("Zurück", on_click=self.previous_step).props("flat outlined").bind_visibility(
                        lambda: self.current_step > 0)
                    ui.button("Weiter", on_click=self.next_step).props("flat outlined").bind_visibility(
                        lambda: self.current_step < len(self.tutorial_steps) - 1)

                ui.button("Tutorial überspringen", on_click=self.skip_tutorial).classes("mt-4")

        ui.on_key("ArrowRight", self.next_step)
        ui.on_key("ArrowLeft", self.previous_step)
        ui.on_swipe("left", self.next_step)
        ui.on_swipe("right", self.previous_step)

        self.update_ui()