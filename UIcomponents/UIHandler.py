import pygame
import pygame_gui as pgui

class UIEventHandler:
    def __init__(self, viz):
        self.viz = viz
    
    def handle(self, event):
        #------------------------------
        # Key strokes handling
        #------------------------------
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.viz.simulation.remove_body()
            if event.key == pygame.K_a:
                self.viz.simulation.add_central_body(
                    mass = 5e24, 
                    position =((self.viz.screen_HW[0]+300)/2, self.viz.screen_HW[1]/2),
                    velocity = (0,0),
                    radius = 25,
                    color = (0,0,255)
                    )
            if event.key == pygame.K_SPACE:
                self.viz.pause = not self.viz.pause
            if event.key == pygame.K_ESCAPE:
                self.viz.running = False
        
        #------------------------------
        # UI Button pressed handling
        #------------------------------
        if event.type == pgui.UI_BUTTON_PRESSED:
            if event.ui_element == self.viz.info_panel.elements["run"]:
                
                self.viz.pause = False
            elif event.ui_element == self.viz.info_panel.elements["pause"]:

                self.viz.pause = True
            elif event.ui_element == self.viz.info_panel.elements["reset"]:
                
                self.viz.bodies.clear()
            elif event.ui_element == self.viz.info_panel.elements["remove"]:
                
                self.viz.simulation.remove_body()
            elif event.ui_element == self.viz.info_panel.elements["add_sat"]:
                if self.viz.input_mode == None:
                    self.viz.input_mode = "Add_satelite"
                else:
                    self.viz.input_mode = None

            elif event.ui_element == self.viz.info_panel.elements["add_cen"]:
                if self.viz.input_mode == None:
                    self.viz.input_mode = "Add_Central"
                    self.viz.info_panel.elements["add_cen"]
                else:
                    self.viz.input_mode = None
        
        #------------------------------
        # Checkbox handling. !! Prototyping !!
        #------------------------------
        if event.type == pygame.USEREVENT and event.user_type == pgui.UI_CHECK_BOX_CHECKED:
            print(f"Checkbox event received for element: {event.ui_element}")
            if event.ui_element == self.viz.info_panel.elements["acc_vec"]:
                self.viz.show_vector_a = True
                print(f"Acceleration vectors toggled: {self.viz.show_vector_a}")
            elif event.ui_element == self.viz.info_panel.elements["vel_vec"]:
                self.viz.show_vector_v = True
                print(f"Velocity vectors toggled: {self.viz.show_vector_v}")

        
        #------------------------------
        # Special button visuals
        #------------------------------
        if self.viz.input_mode == "Add_satelite":
            self.viz.info_panel.elements["add_sat"].select()
            self.viz.info_panel.elements["add_cen"].unselect()
        elif self.viz.input_mode == "Add_Central":
            self.viz.info_panel.elements["add_cen"].select()
            self.viz.info_panel.elements["add_sat"].unselect()
        # else:
        #     self.viz.info_panel.elements["add_sat"].unselect()
        #     self.viz.info_panel.elements["add_cen"].unselect()



                