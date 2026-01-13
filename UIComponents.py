import pygame
import pygame_gui as pgui

CENTER_X = 810
CENTER_Y = 360
class UIComponents:

    def __init__(self, viz):
        self.viz = viz
        self.manager = self.viz.Uim
        self.screen_size = self.viz.screen_HW
        self.panel = {}
        self.selected_bodyPanel = None
        self.elements = {}   # store everything here

    # -------------------------
    # Main PANEL
    # -------------------------
    def create_panel(self, name, pos=(0, 0), size=(300, 720)):
        self.panel[name] = pgui.elements.UIPanel(
            relative_rect=pygame.Rect(pos, size),
            manager=self.manager
        )
        return self.panel
    
    # #--------------------------
    # # PANEL
    # #--------------------------
    # def create_panel(self, pos=(0,0), size = (300, 375)):
    #     panel = pgui.elements.UIPanel(
    #         relative_rect=pygame.Rect(pos, size),
    #         manager=self.manager
    #     )
    #     return panel

    # -------------------------
    # BUTTON
    # -------------------------
    def button(self, name, text, pos, size=(200, 40), objectID = "button", container = None):
        container = self.panel["main"] if not container else container
        self.elements[name] = pgui.elements.UIButton(
            relative_rect=pygame.Rect(pos, size),
            text=text,
            manager=self.manager,
            container= container,
            object_id= objectID
        )
        return self.elements[name]

    # -------------------------
    # SLIDER
    # -------------------------
    def slider(self, name, pos, size, value_range=(0, 100), start=50, container = None):
        container = self.panel["main"] if not container else container
        self.elements[name] = pgui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(pos, size),
            start_value=start,
            value_range=value_range,
            manager=self.manager,
            container= container
        )
        return self.elements[name]

    # -------------------------
    # CHECKBOX
    # -------------------------
    def checkbox(self, name, text, pos, container = None):
        container = self.panel["main"] if not container else container
        self.elements[name] = pgui.elements.UICheckBox(
            relative_rect=pygame.Rect(pos, (20, 20)),
            text=text,
            manager=self.manager,
            container= container
        )
        return self.elements[name]

    # -------------------------
    # LABEL
    # -------------------------
    def label(self, name, text, pos, size=(200, 30), container = None):
        container = self.panel["main"] if not container else container
        self.elements[name] = pgui.elements.UILabel(
            relative_rect=pygame.Rect(pos, size),
            text=text,
            manager=self.manager,
            container= container
        )
        return self.elements[name]
    # -------------------------
    # Text Box
    # -------------------------
    def textBox(self, name, pos, size=(180, 30), container = None):
        container = self.panel["main"] if not container else container
        self.elements[name] = pgui.elements.UITextEntryLine(
            relative_rect= pygame.Rect(pos, size),
            manager= self.manager,
            container= container
        )
        return self.elements[name]
    # -------------------------
    # MASTER BUILD FUNCTION
    # -------------------------
    def build(self):
        """Create your entire UI layout here"""

        self.create_panel("main")

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
        self.checkbox("grid_mode", "Show grid", (10, y))
        y += gap_y//2
        self.checkbox("dist_mode", "Show distances", (10, y))
        y += gap_y//2


        return self

    def selected_body_panel(self, b):
        self.selected_body_panel_kill()
        self.create_panel("mass_prop", (1020,0),(300,400))
        y = 0

        self.label("mass_properties", "Selected Mass properties", (50, y), (200,30), self.panel["mass_prop"])
        y += 35
        gap_y = 45


        self.label("mass_lbl", "Mass: ", (-70, y), (200, 30), self.panel["mass_prop"])
        self.textBox("Mass_textBox", (60, y), (180,30), self.panel["mass_prop"])
        self.elements["Mass_textBox"].set_text(str(b.mass))
        self.label("mass_lblUnits", "Kg", (160, y), (200, 30), self.panel["mass_prop"])
        y += gap_y - 15

        self.label("radius_lbl", "Radius: ", (-70, y), (200, 30), self.panel["mass_prop"])
        self.textBox("Rad_textBox", (60, y), (180, 30), self.panel["mass_prop"])
        self.elements["Rad_textBox"].set_text(str(b.radius))
        self.label("rad_lblUnits", "Pixels", (160, y), (200, 30), self.panel["mass_prop"])
        y += gap_y - 15

        self.label("velocoty_lbl", "Velocity (m/s): ", (-45, y), (200, 30), self.panel["mass_prop"])
        y += gap_y - 15
        self.label("vel_x_lbl", "x:", (-30, y), (90,30), self.panel["mass_prop"])
        self.textBox("vel_x_txtB", (23, y), (90,30), self.panel["mass_prop"])
        self.elements["vel_x_txtB"].set_text(str(round(b.velocity[0], 2))),
        self.label("vel_y_lbl", "y:", (80, y), (90,30), self.panel["mass_prop"])
        self.textBox("vel_y_txtB", (133, y), (90,30), self.panel["mass_prop"])
        self.elements["vel_y_txtB"].set_text(str(round(b.velocity[1],2)))
        y += gap_y -15

        self.checkbox("perfect_Orbit", "Get perfect satellite orbit", (10, y), self.panel["mass_prop"])
        y += gap_y//2


        self.label("Position_lbl", "Position: ", (-60, y), (200, 30), self.panel["mass_prop"])
        y += gap_y-15
        self.label("pos_x_lbl", "x:", (-30, y), (90,30), self.panel["mass_prop"])
        self.textBox("pos_x_txtB", (23, y), (90,30), self.panel["mass_prop"])
        self.elements["pos_x_txtB"].set_text(str(round(b.position[0]+510, 2)))
        self.label("pos_y_lbl", "y:", (80, y), (90,30), self.panel["mass_prop"])
        self.textBox("pos_y_txtB", (133, y), (90,30), self.panel["mass_prop"])
        self.elements["pos_y_txtB"].set_text(str(round(b.position[1]-360,2)))
        y += gap_y - 15

        self.button("upd_MassRad", "Enter", (220,y), (67, 40), "button", self.panel["mass_prop"])
        y += gap_y - 5

        self.checkbox("vel_grh", "Generate velocity graph", (10, y),self.panel["mass_prop"])
        y += gap_y//2
        self.checkbox("acc_grh", "Generate acceleration graph", (10, y), self.panel["mass_prop"])
        y += gap_y//2
        self.checkbox("E_grh", "Generate Energy graph", (10,y), self.panel["mass_prop"])
        y += gap_y//2
        
        
        if b.mass > 5e11:
            self.elements["perfect_Orbit"].disable()
        if len(self.viz.simulation.centralBodies) >= 2:
            self.elements["perfect_Orbit"].disable()
        
    
    def selected_body_panel_kill(self):
        if "mass_prop" in self.panel:
            self.panel["mass_prop"].kill()
    
    def update_selected_body_panel(self, b):
        if b is None:
            return

        if "pos_x_txtB" not in self.elements:
            return
        # IMPORTANT: only update if user is NOT typing
        if not self.elements["pos_x_txtB"].is_focused:
            self.elements["pos_x_txtB"].set_text(str(round(b.position[0] - CENTER_X, 2)))

        if not self.elements["pos_y_txtB"].is_focused:
            self.elements["pos_y_txtB"].set_text(str(round(CENTER_Y - b.position[1], 2)))
