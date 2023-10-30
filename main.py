from pyray import *
import random
import os
import math

WIDTH = 1400
HEIGHT = 800
TITLE = "2D Aim Trainer"
init_window(WIDTH,HEIGHT,TITLE)

crosshair_position = Vector2(-100,-100)
crosshair_color = (255,255,255,255)
custom_font = load_font(str(os.path.abspath('Raleway-Bold.ttf')),44)
init_audio_device()
hit_sound = load_music_stream('soft-notice-146623.mp3')
play_music = True
volume_on_image = load_texture_from_image( load_image('volume.png') )
volume_off_image = load_texture_from_image( load_image('volume_off.png') )
volume = True
volume_button_x = 1200
volume_button_y = 80
button_bounds = Rectangle(volume_button_x,volume_button_y,100,100)
menu = True


class Target:
    def __init__(self,position,color=None) -> None:
        self.target_position = position 
        self.target_color = YELLOW 
        self.target_radius = 5
    def deploy(self): 
        draw_circle(int(self.target_position.x) , int(self.target_position.y),self.target_radius,self.target_color)

targets = [Target(Vector2(random.randint(20,1200) , random.randint(20,700))) for i in range(5)]
score = 0
set_target_fps(120)

while not window_should_close():

    begin_drawing()
    clear_background(BLACK)
    if menu:
        show_cursor()
        clear_background(PURPLE)
        
        draw_text_ex(custom_font,'Press Mouse Left To Start' ,Vector2(100,100),54,9,RAYWHITE)
        if volume:
            draw_texture_ex(volume_on_image,Vector2(volume_button_x,volume_button_y),0,0.2,WHITE)
        else:
            draw_texture_ex(volume_off_image,Vector2(volume_button_x,volume_button_y),0,0.2,WHITE)
        if check_collision_point_rec(get_mouse_position(),button_bounds)and is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
            volume  = not volume
            play_music = not play_music
            
            # draw_rectangle(volume_button_x,volume_button_y,100,100,WHITE)
            
        elif is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
            menu=False
    else:
        update_music_stream(hit_sound)
        hide_cursor()
        clear_background(VIOLET)
        draw_text_ex(custom_font,f'press q to go to menu FPS:{get_fps()} SCORE:{score} ',Vector2(10,30),22,4,(250, 249, 246,255))
        for target in targets:
            target.deploy()

        crosshair_position.x = get_mouse_position().x
        crosshair_position.y = get_mouse_position().y
        crosshair = draw_circle(int(crosshair_position.x),int(crosshair_position.y),3,WHITE)

        for target in targets:
            if check_collision_circles(crosshair_position,3,target.target_position,target.target_radius) and is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
                targets.remove(target)
                if play_music:
                    play_music_stream(hit_sound)
                targets.append(Target(Vector2(random.randint(100,1200) , random.randint(100,700))))
                score+=1
            if play_music:
                if get_music_time_played(hit_sound)>0.5:
                    stop_music_stream(hit_sound)
        if is_key_pressed(KeyboardKey.KEY_Q):
            menu=True
        
        
    end_drawing()

close_window()