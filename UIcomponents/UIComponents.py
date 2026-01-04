import pygame
import pygame_gui as pgui


class UIComponents:
    def __init__(self, manager, screen_size):
        self.manager = manager
        self.screen_size = screen_size
        self.panel = None
        self.elements = {}   # store everything here

    # -------------------------
    # PANEL
    # -------------------------
    def create_panel(self, pos=(0, 0), size=(300, 720)):
        self.panel = pgui.elements.UIPanel(
            relative_rect=pygame.Rect(pos, size),
            manager=self.manager
        )
        return self.panel

    # -------------------------
    # BUTTON
    # -------------------------
    def button(self, name, text, pos, size=(200, 40), objectID = "button"):
        self.elements[name] = pgui.elements.UIButton(
            relative_rect=pygame.Rect(pos, size),
            text=text,
            manager=self.manager,
            container=self.panel,
            object_id= objectID
        )
        return self.elements[name]

    # -------------------------
    # SLIDER
    # -------------------------
    def slider(self, name, pos, size, value_range=(0, 100), start=50):
        self.elements[name] = pgui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(pos, size),
            start_value=start,
            value_range=value_range,
            manager=self.manager,
            container=self.panel
        )
        return self.elements[name]

    # -------------------------
    # CHECKBOX
    # -------------------------
    def checkbox(self, name, text, pos):
        self.elements[name] = pgui.elements.UICheckBox(
            relative_rect=pygame.Rect(pos, (20, 20)),
            text=text,
            manager=self.manager,
            container=self.panel
        )
        return self.elements[name]

    # -------------------------
    # LABEL
    # -------------------------
    def label(self, name, text, pos, size=(200, 30)):
        self.elements[name] = pgui.elements.UILabel(
            relative_rect=pygame.Rect(pos, size),
            text=text,
            manager=self.manager,
            container=self.panel
        )
        return self.elements[name]
    # -------------------------
    # Text Box
    # -------------------------
    def textBox(self, name, pos, size=(180, 30)):
        self.elements[name] = pgui.elements.UITextEntryLine(
            relative_rect= pygame.Rect(pos, size),
            manager= self.manager,
            container=self.panel
        )
        return self.elements[name]
    # -------------------------
    # MASTER BUILD FUNCTION
    # -------------------------
    def build(self):
        """Create your entire UI layout here"""

        self.create_panel()

        y = 10
        gap_y = 45

        self.label("Topic", "N-Body Simulation", (50, y))
        y += gap_y
        self.button("run", "Run", (10,y), (67, 40))
        self.button("pause", "Pause", (85,y), (67, 40))
        self.button("reset", "Reset", (160,y), (67, 40), "#Clearbodies_button")
        y += gap_y
        self.button("add_sat", "Add Satellite body", (10, y), (216,40))
        y += gap_y
        self.button("add_cen", "Add Major body", (10, y), (216,40))
        y += gap_y
        self.button("remove", "Remove Body", (10, y), (216,40))
        y += gap_y+15

        self.checkbox("vel_vec", "Show Velocity vector", (10, y))
        y += gap_y//2
        self.checkbox("acc_vec", "Show Acceleration vector", (10, y))
        y += gap_y//2
        self.checkbox("perfect_Orbit", "Get perfect satellite orbit", (10, y))
        y += gap_y//2
        # self.checkbox("perfect_vel_chB", "Perfect circular orbits (single central body only)", (10,y))
        y = 400

        self.label("mass_properties", "Selected Mass properties", (50, y))
        y += 35

        self.label("mass_lbl", "Mass: ", (-70, y))
        self.textBox("Mass_textBox", (60, y))
        self.label("mass_lblUnits", "Kg", (160, y))
        y += gap_y - 15

        self.label("radius_lbl", "Radius: ", (-70, y))
        self.textBox("Rad_textBox", (60, y))
        self.label("rad_lblUnits", "Pixels", (160, y))
        y += gap_y - 15

        self.label("velocoty_lbl", "Velocity (m/s): ", (-45, y))
        y += gap_y - 15
        self.label("vel_x_lbl", "x:", (-30, y), (90,30))
        self.textBox("vel_x_txtB", (23, y), (90,30))
        self.label("vel_y_lbl", "y:", (80, y), (90,30))
        self.textBox("vel_y_txtB", (133, y), (90,30))
        y += gap_y -15

        self.label("Acceleration_lbl", "Acceleration (m^2/s): ", (-20, y))
        y += gap_y-15
        self.label("acc_x_lbl", "x:", (-30, y), (90,30))
        self.textBox("acc_x_txtB", (23, y), (90,30))
        self.label("acc_y_lbl", "y:", (80, y), (90,30))
        self.textBox("acc_y_txtB", (133, y), (90,30))
        y += gap_y - 5

        self.checkbox("vel_grh", "Generate velocity graph", (10, y))
        y += gap_y//2
        self.checkbox("acc_grh", "Generate acceleration graph", (10, y))
        y += gap_y//2
        self.checkbox("E_grh", "Generate Energy graph", (10,y))
        y += gap_y//2


        # self.slider("mass", (10, y), (200, 20), (1, 100), 10)

        return self
