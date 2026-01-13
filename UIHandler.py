
#UIHandler.py
import pygame
import pygame_gui as pgui
from physics import body
import numpy as np

class UIEventHandler:
    def __init__(self, viz):
        self.viz = viz
    
    def handle(self, event):

        self.handle_keyStrokes(event)

        self.handle_UIbutton(event)

        self.handle_checkBox(event)

        self.handle_mouse_drag(event)
        #------------------------------
        # Special button visuals
        #------------------------------
        if self.viz.input_mode == "Add_satelite":
            self.viz.info_panel.elements["add_sat"].select()
            self.viz.info_panel.elements["add_cen"].unselect()
        elif self.viz.input_mode == "Add_Central":
            self.viz.info_panel.elements["add_cen"].select()
            self.viz.info_panel.elements["add_sat"].unselect()

        if not self.viz.pause:
            self.viz.info_panel.elements["add_sat"].disable()
            self.viz.info_panel.elements["add_cen"].disable()
            self.viz.info_panel.elements["remove"].disable()
            self.viz.info_panel.elements["run"].select()
            self.viz.info_panel.elements["pause"].unselect()

        else:
            self.viz.info_panel.elements["add_sat"].enable()
            self.viz.info_panel.elements["add_cen"].enable()
            self.viz.info_panel.elements["remove"].enable()
            self.viz.info_panel.elements["pause"].select()
            self.viz.info_panel.elements["run"].unselect()

    def handle_keyStrokes(self, event):
        #------------------------------
        # Key strokes handling
        #------------------------------
        if event.type == pygame.KEYDOWN:
            # if event.key == pygame.K_BACKSPACE:
            #     # self.viz.simulation.remove_body()
            if event.key == pygame.K_SPACE:
                self.viz.pause = not self.viz.pause
            elif event.key == pygame.K_ESCAPE:
                self.viz.running = False
    
    def handle_UIbutton(self, event):
        #------------------------------
        # UI Button pressed handling
        #------------------------------
        if event.type == pgui.UI_BUTTON_PRESSED:
            if event.ui_element == self.viz.info_panel.elements["run"]:
                self.viz.UIBuilder.selected_body_panel_kill()
                self.viz.simulation.unselectBodies()
                self.viz.pause = False

            elif event.ui_element == self.viz.info_panel.elements["pause"]:
                self.viz.UIBuilder.selected_body_panel_kill()
                self.viz.simulation.unselectBodies()
                self.viz.pause = True

            elif event.ui_element == self.viz.info_panel.elements["reset"]:
                self.viz.UIBuilder.selected_body_panel_kill()
                self.viz.simulation.unselectBodies()
                self.viz.simulation.remov_every_body()

            elif event.ui_element == self.viz.info_panel.elements["remove"]:

                self.viz.simulation.remove_body()
                self.viz.UIBuilder.selected_body_panel_kill()

            elif event.ui_element == self.viz.info_panel.elements["add_sat"]:
                body.unselect_body(self.viz.bodies)
                self.viz.UIBuilder.selected_body_panel_kill()
                if self.viz.input_mode == None:
                    self.viz.input_mode = "Add_satelite"
                else:
                    self.viz.input_mode = None

            elif event.ui_element == self.viz.info_panel.elements["add_cen"]:
                body.unselect_body(self.viz.bodies)
                self.viz.UIBuilder.selected_body_panel_kill()
                if self.viz.input_mode == None:
                    self.viz.input_mode = "Add_Central"
                    self.viz.info_panel.elements["add_cen"]
                else:
                    self.viz.input_mode = None
            elif event.ui_element == self.viz.info_panel.elements["upd_MassRad"]:
                userinput = [self.viz.info_panel.elements["Mass_textBox"].get_text(), 
                             self.viz.info_panel.elements["Rad_textBox"].get_text(),
                             self.viz.info_panel.elements["vel_x_txtB"].get_text(),
                             self.viz.info_panel.elements["vel_y_txtB"].get_text()]
                b = self.viz.simulation.getSelectedbody()
                try:
                    if userinput[0] != '':
                        b.mass = float(userinput[0])
                    if userinput[1] != '':
                        b.radius = int(userinput[1])
                    if userinput[2] != '':
                        b.velocity[0] = float(userinput[2])
                    if userinput[3] != '':
                        b.velocity[1] = float(userinput[3])
                except ValueError:
                    print("Invalid input! Please enter a number.")
                    self.viz.info_panel.elements["Mass_textBox"].set_text(str(b.mass))
                    self.viz.info_panel.elements["Rad_textBox"].set_text(str(b.radius))
                    self.viz.info_panel.elements["vel_x_txtB"].set_text(str(b.velocity[0]))
                    self.viz.info_panel.elements["vel_y_txtB"].set_text(str(b.velocity[1]))
    def handle_checkBox(self, event):
        #------------------------------
        # Checkbox handling. !! Prototyping !!
        #------------------------------
        if event.type == pgui.UI_CHECK_BOX_CHECKED:
            if event.ui_element == self.viz.info_panel.elements["acc_vec"]:
                print("acceleration checkbox toggeles")
                self.viz.show_vector_a = not self.viz.show_vector_a

            elif event.ui_element == self.viz.info_panel.elements["vel_vec"]:
                print("velocity checkbox toggeles")
                self.viz.show_vector_v = not self.viz.show_vector_v

            elif event.ui_element == self.viz.info_panel.elements["grid_mode"]:
                self.viz.show_grid = not self.viz.show_grid
            elif event.ui_element == self.viz.info_panel.elements["dist_mode"]:
                self.viz.show_distance = not self.viz.show_distance
            elif "perfect_Orbit" in self.viz.info_panel.elements \
             and event.ui_element == self.viz.info_panel.elements["perfect_Orbit"]:
            
                vel = self.viz.simulation.getPOrbit()
                self.viz.info_panel.elements["vel_x_txtB"].set_text(str(round(vel[0], 2)))
                self.viz.info_panel.elements["vel_y_txtB"].set_text(str(round(vel[1], 2)))
            

        if event.type == pgui.UI_CHECK_BOX_UNCHECKED:
            if event.ui_element == self.viz.info_panel.elements["acc_vec"]:
                print("acceleration checkbox toggeles")
                self.viz.show_vector_a = not self.viz.show_vector_a

            elif event.ui_element == self.viz.info_panel.elements["vel_vec"]:
                print("velocity checkbox toggeles")
                self.viz.show_vector_v = not self.viz.show_vector_v
            elif event.ui_element == self.viz.info_panel.elements["grid_mode"]:
                self.viz.show_grid = not self.viz.show_grid
            elif event.ui_element == self.viz.info_panel.elements["dist_mode"]:
                self.viz.show_distance = not self.viz.show_distance

    
    def handle_mouse_drag(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            if not self.viz.pause:
                return
            if self.viz.mouse_over_ui():
                self.viz.input_mode = None
                self.viz.info_panel.elements["add_sat"].unselect()
                self.viz.info_panel.elements["add_cen"].unselect()
                return
            pos = event.pos
            if pos[0] < 300:
                if self.viz.input_mode is not None:
                    self.viz.input_mode = None
                    self.viz.info_panel.elements["add_sat"].unselect()
                    self.viz.info_panel.elements["add_cen"].unselect()
                return
            new_mode = self.viz.simulation.handle_click(pos, self.viz.input_mode)

            # If we were adding a body, do NOT select or drag anything 
            if self.viz.input_mode is not None:
                self.viz.input_mode = new_mode
                return

            self.viz.input_mode = new_mode

            for b in self.viz.simulation.bodies:
                dx = b.position[0] - pos[0]
                dy = b.position[1] - pos[1]
                distance = (dx**2 + dy**2)**0.5
                if distance <= b.radius:
                    self.viz.dragging_body = b
                    self.viz.drag_offset = (b.position[0]-pos[0], b.position[1]-pos[1])
                    b.selected = True
                    b.dragging = True
                    b.trail.clear()   # IMPORTANT: reset old trail
                    break
                
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.viz.dragging_body:
                self.viz.dragging_body.dragging = False
            self.viz.dragging_body = None

        elif event.type == pygame.MOUSEMOTION:
            if self.viz.dragging_body:
                mx, my = event.pos
                ox, oy = self.viz.drag_offset
                self.viz.dragging_body.position = np.array([mx + ox, my + oy])
                # Optional: reset velocity while dragging so physics doesn't fight you
                self.viz.dragging_body.velocity = np.array([0.0, 0.0])