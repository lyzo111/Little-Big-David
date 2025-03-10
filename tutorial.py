from nicegui import ui


class Tutorial:
    def __init__(self):
        """
        Initialize the Tutorial class with the current step set to 0 and predefined tutorial steps.
        """
        self.current_step = 0
        self.tutorial_steps = [
            {"title": "Welcome to Little Big David!",
             "description": "Little Big David is an adventure where you complete tasks to strengthen your character. "
                            "Explore the world, defeat enemies, and collect items!"},
            {"title": "Your First Task",
             "description": "David is still small. He needs XP to grow. Complete daily tasks like 'Meditate for 10 minutes' or 'Take a walk' to become stronger."},
            {"title": "Battles and Buffs",
             "description": "David can defeat enemies to gain buffs or take alternative paths to collect items. "
                            "The goal is to become strong enough to defeat the final bosses!"},
            {"title": "Retirement System",
             "description": "When David is strong enough, he can retire. But be careful: After retirement, his stats will be reset. "
                            "However, he will receive rewards like new abilities or rare equipment!"},
            {"title": "Main and Side Quests",
             "description": "Complete main quests to advance the story, or explore the world for side quests to find treasures and buffs."},
            {"title": "Finished!",
             "description": "Now you are ready to send David on his adventure! Have fun playing Little Big David."}
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
                ui.label("Do your really want to skip the tutorial?")
                with ui.row().classes("justify-around mt-4"):
                    ui.button("Yes, please", on_click=lambda: self.end_tutorial(dialog))
                    ui.button("Oh hell no", on_click=dialog.close)


    def end_tutorial(self, dialog):
        """
        End the tutorial, close the dialog, and clear the tutorial UI.
        """
        dialog.close()
        ui.notify("Tutorial finished!")
        self.tutorial_ui.clear()
        with self.tutorial_ui:
            ui.label("Once again, welcome to Little Big David! Have fun growing!").classes("text-xl font-bold mt-10")
        from src.gui import gui
        gui.initialize_gui()


    def update_ui(self):
        """
        Update the UI elements to reflect the current step in the tutorial.
        """
        step = self.tutorial_steps[self.current_step]
        self.title.content = step["title"]
        self.description.content = step["description"]
        # Update progress bar here


    def show(self):
        """
        Display the tutorial UI with navigation buttons and progress bar.
        """
        with ui.column().classes("items-center justify-center") as self.tutorial_ui:
            # Back button
            # ui.button("Back", on_click=self.previous_step).props("flat outlined").bind_visibility(
            #     lambda: self.current_step > 0)

            # Tutorial content
            with ui.card().classes("w-1/2"):
                self.title = ui.label().classes("text-xl font-bold mb-4")
                self.description = ui.label().classes("mb-4")
                # Add progress bar here

                with ui.row().classes("justify-around"):
                    ui.button("Back", on_click=self.previous_step).props("flat outlined").bind_visibility(
                        lambda: self.current_step > 0)
                    ui.button("Next", on_click=self.next_step).props("flat outlined").bind_visibility(
                        lambda: self.current_step < len(self.tutorial_steps) - 1)

                ui.button("Skip Tutorial", on_click=self.skip_tutorial).classes("mt-4")

            # Next button
            # ui.button("Next", on_click=self.next_step).props("flat outlined").bind_visibility(
            #     lambda: self.current_step < len(self.tutorial_steps) - 1)

        self.update_ui()
