import pygame as py,sys,random
from pygame.locals import *
from pygame import mixer
py.init() 
mixer.init()
die_sound=mixer.Sound('audio/die.ogg')
fly=mixer.Sound('audio/wing.ogg')
#variables
screen_width=576
screen_height=512
x=30
y=screen_height//2
bird_move=0
win=py.display.set_mode((screen_width,screen_height))
clock=py.time.Clock()
jump_count=7
is_jump=False
gravity=0.1
is_gravity=False
game_status=True
menu_status=True
score_status=False
play_key_status=False
mouse_status=False
keyboard_status=False
difficulty_status=False
start_key=False


#loading images
bg=py.image.load('sprites/background-day.png')

f=py.image.load('sprites/base.png')

bird=py.image.load('sprites/bluebird-downflap.png')
bird_rect=bird.get_rect(center=(x,y))

pipe=py.image.load('sprites/pipe-red.png')
# pipe_rect=pipe.get_rect(center=(x,y))


#transform
new_bbg=py.transform.scale(bg,(576,512))
new_bg=new_bbg.get_rect(topleft=(0,0))
floor=py.transform.scale(f,(576,80))
floor_x=0
#pipe spawn
SPAWN=py.USEREVENT
py.time.set_timer(SPAWN,1200)
pipe_list=[]
pipe_height=[240,300,350,390]
#text
font = py.font.Font('04B_19.ttf', 32)
text_play = font.render('PLAY',True,(255,255,255))
play_rect = text_play.get_rect(center = (288,60))

text_score = font.render('SCORE',True,(255,255,255))
score_rect = text_play.get_rect(center = (288,100))

text_score_value=font.render(':'+'69',True,(255,255,255))
score_value_rect=text_score_value.get_rect(center=(390,100))

text_choose = font.render('CHOOSE DEVICE TO PLAY :-',True,(255,255,255))
choose_rect = text_play.get_rect(center = (120,100))

text_mouse = font.render('mouse',True,(255,255,255))
mouse_rect= text_play.get_rect(center = (100,230))

text_keyboard = font.render('keyboard',True,(255,255,255))
keyboard_rect = text_play.get_rect(center = (430,230))

text_difficulty = font.render('difficulty->',True,(255,255,255))
difficulty_rect = text_play.get_rect(center = (250,140))

text_easy = font.render('easy',True,(255,255,255))
easy_rect = text_play.get_rect(center = (440,140))

text_hard = font.render('hard',True,(255,255,255))
hard_rect = text_play.get_rect(center = (440,140))

text_press = font.render('press click or space ro start',True,(255,255,255))
press_rect = text_play.get_rect(center = (100,100))


#functions
def create_pipe(pipe):
    n=random.choice(pipe_height)
    new_bp=pipe.get_rect(midtop=(576,n))
    new_tp=pipe.get_rect(midbottom=(576,n-random.randint(100,200)))
    return new_tp,new_bp
def move_pipe(pipe_list):
    for p in pipe_list:
        p.centerx-=5
    return pipe_list
def collide(pipe_list):
    for p in pipe_list:
        if bird_rect.colliderect(p):
           die_sound.play()
           return False
    if bird_rect.top<=-50 or bird_rect.bottom>= screen_height-80:
        die_sound.play()
        return False
    return True

def draw(pipe_list):
    global floor_x
    #pipe draw
    pipe_list=move_pipe(pipe_list)
    for p in pipe_list:
        if p.bottom>500:
            win.blit(pipe,p)
        else:
            flip_pipe=py.transform.flip(pipe,False,True)
            win.blit(flip_pipe,p)
    win.blit(bird,bird_rect)
    floor_x-=1
    win.blit(floor,(floor_x,screen_height-80))
    win.blit(floor,(floor_x+576,screen_height-80))
    if(floor_x<-576):
        floor_x=0
    
    py.display.update()
    if difficulty_status:
        clock.tick(140)
    else:
        clock.tick(90)

#mian loop
while(1):
    if not menu_status :    
        for event in py.event.get():
            if event.type==QUIT:
                py.quit()
                sys.exit()
            if event.type==KEYDOWN and keyboard_status:
                if event.key==K_SPACE and game_status:
                    bird_move=0
                    bird_move-=3
                    fly.play()
                if event.key== K_SPACE and not(game_status):
                    game_status=True
                    pipe_list.clear()
                    bird_rect.center=(x,y)
                    bird_move=0
            if event.type== py.MOUSEBUTTONUP and mouse_status:
                if new_bg.collidepoint(event.pos) and game_status:
                    bird_move=0
                    bird_move-=3
                    fly.play()
                if new_bg.collidepoint(event.pos) and not(game_status):
                    game_status=True
                    pipe_list.clear()
                    bird_rect.center=(x,y)
                    bird_move=0
            if event.type==SPAWN:
                pipe_list.extend(create_pipe(pipe))
        win.blit(new_bbg,new_bg)
        if game_status:
            bird_move+=gravity
            bird_rect.centery+=bird_move
            draw(pipe_list)
            game_status=collide(pipe_list)
    if menu_status:
        for event in py.event.get():
            if event.type==QUIT:
                py.quit()
                sys.exit()
            if event.type==py.MOUSEBUTTONDOWN:
                if (play_rect.collidepoint(event.pos)):
                    play_key_status=True
                if (score_rect.collidepoint(event.pos)):
                    if score_status:
                        score_status=False
                    else:
                        score_status=True
                if(mouse_rect.collidepoint(event.pos)):
                    menu_status=False
                    mouse_status=True
                    
                if( keyboard_rect.collidepoint(event.pos)):
                    menu_status=False
                    keyboard_status=True
                    
                if( difficulty_rect.collidepoint(event.pos)):
                    if difficulty_status: 
                        difficulty_status=False
                    else:
                        difficulty_status=True
        if not play_key_status:
            win.blit(new_bbg,new_bg)
            win.blit(text_play,play_rect)
            win.blit(text_score,score_rect)
            win.blit(text_difficulty,difficulty_rect)
            if difficulty_status:
                win.blit(text_hard,hard_rect)
            else:
                win.blit(text_easy,easy_rect)
            if score_status:
                win.blit(text_score_value,score_value_rect)
        else:
            win.fill((0,0,0))
            win.blit(new_bbg,new_bg)
            win.blit(text_choose,choose_rect)
            win.blit(text_keyboard,keyboard_rect)
            win.blit(text_mouse,mouse_rect)
        py.display.update()

          