
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

    def handle_keyStrokes(self, event):
        #------------------------------
        # Key strokes handling
        #------------------------------
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.viz.simulation.remove_body()
            elif event.key == pygame.K_SPACE:
                self.viz.pause = not self.viz.pause
            elif event.key == pygame.K_ESCAPE:
                self.viz.running = False
    
    def handle_UIbutton(self, event):
        #------------------------------
        # UI Button pressed handling
        #------------------------------
        if event.type == pgui.UI_BUTTON_PRESSED:
            if event.ui_element == self.viz.info_panel.elements["run"]:
                
                self.viz.pause = False
            elif event.ui_element == self.viz.info_panel.elements["pause"]:

                self.viz.pause = True
            elif event.ui_element == self.viz.info_panel.elements["reset"]:
                self.viz.simulation.remov_every_body()
            elif event.ui_element == self.viz.info_panel.elements["remove"]:
                
                self.viz.simulation.remove_body()
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
        if event.type == pgui.UI_CHECK_BOX_UNCHECKED:
            if event.ui_element == self.viz.info_panel.elements["acc_vec"]:
                print("acceleration checkbox toggeles")
                self.viz.show_vector_a = not self.viz.show_vector_a

            elif event.ui_element == self.viz.info_panel.elements["vel_vec"]:
                print("velocity checkbox toggeles")
                self.viz.show_vector_v = not self.viz.show_vector_v
    
    def handle_mouse_drag(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            pos = event.pos
            for b in self.viz.simulation.bodies:
                dx = b.position[0] - pos[0]
                dy = b.position[1] - pos[1]
                distance = (dx**2 + dy**2)**0.5
                if distance <= b.radius:
                    self.viz.dragging_body = b
                    self.viz.drag_offset = (b.position[0]-pos[0], b.position[1]-pos[1])
                    b.selected = True
                    break
                
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.viz.dragging_body = None

        elif event.type == pygame.MOUSEMOTION:
            if self.viz.dragging_body:
                mx, my = event.pos
                ox, oy = self.viz.drag_offset
                self.viz.dragging_body.position = np.array([mx + ox, my + oy])
                # Optional: reset velocity while dragging so physics doesn't fight you
                self.viz.dragging_body.velocity = np.array([0.0, 0.0])
