#####################################
# Answer Button
##################################### 

# Call this label before you show a menu
# to show the answer button
label answer(from_cg=False): 
    # Check if it's from the messenger or a text message
    if not text_person:
        if from_cg:
            hide screen viewCG
        else:
            $ pauseFailsafe()   
        $ pre_choosing = True
        call screen answer_button
        show screen pause_button
    # Otherwise it's a real-time text conversation
    else:
        if from_cg:
            hide screen viewCG
        else:
            $ text_pauseFailsafe(text_person.text_msg.msg_list)
        $ pre_choosing = True
        call screen text_answer
        show screen text_pause_button
            
    return
        
screen answer_button():
    zorder 4
    tag chat_footer
    add 'pause_square' yalign 0.59
    if persistent.custom_footers:
        add 'custom_pausebutton' xalign 0.96 yalign 0.16
        add 'custom_answerbutton' ypos 1220
    else:
        add "pausebutton" xalign 0.96 yalign 0.16
        add "answerbutton" ypos 1220
    
    imagebutton:
        ypos 1220
        focus_mask None
        idle 'transparent_answer'
        activate_sound "audio/sfx/UI/answer_screen.mp3"
        action [Show('pause_button'), Return()] 

    if not choosing:
        # Fast button
        imagebutton:
            xalign 0.985
            yalign 0.997
            focus_mask None
            idle "fast_slow_button"
            action [Function(fast_pv), 
                    Hide('speed_num'), 
                    Show("speed_num")]
                
        # Slow button
        imagebutton:
            xalign 0.015
            yalign 0.997
            focus_mask None
            idle "fast_slow_button"
            action [Function(slow_pv), 
                    Hide('speed_num'), 
                    Show("speed_num")]

    
#####################################
# Pause/Play footers
#####################################
   
# This is the screen that shows the pause button
# (but the chat is still playing)
screen pause_button():
    zorder 4
    tag chat_footer
    
    imagebutton:
        ypos 1220
        focus_mask True
        idle 'phone_pause'
        if not choosing:
            action [Call("play"), Return()]
     
    if not choosing:
        # Fast button
        imagebutton:
            xalign 0.985
            yalign 0.997
            focus_mask None
            idle "fast_slow_button"
            action [Function(fast_pv), 
                    Hide('speed_num'), 
                    Show("speed_num")]
                
        # Slow button
        imagebutton:
            xalign 0.015
            yalign 0.997
            focus_mask None
            idle "fast_slow_button"
            action [Function(slow_pv), 
                    Hide('speed_num'), 
                    Show("speed_num")]
        
# This is automatically called when you pause the chat;
# it makes sure no messages are skipped        
label play():
    if (observing and not vn_choice and not text_msg_reply 
            and not in_phone_call and not email_reply):
        # We're rewatching a chatroom
        call screen play_button
        show screen pause_button
        $ replay_from = chatroom_replay_index
        jump chatroom_replay
    if not text_person:
        #$ chatlog.append(ChatEntry(chat_pause,'',upTime()))
        call screen play_button
        show screen pause_button
    else:
        call screen text_play_button
        show screen text_pause_button
    return
    
# This screen is visible when the chat is paused;
# shows the play button
screen play_button():
    zorder 4
    tag chat_footer
    if not choosing:
        if persistent.custom_footers:
            add 'custom_pausebutton' xalign 0.96 yalign 0.16
        else:
            add "pausebutton" xalign 0.96 yalign 0.16
        add "pause_square" yalign 0.59
    imagebutton:
        xanchor 0.0
        yanchor 0.0
        xpos 0
        ypos 1220
        focus_mask True
        idle 'phone_play'
        action [Show('pause_button'), Return()]
    
    if not choosing:
        # Fast button
        imagebutton:
            xalign 0.985
            yalign 0.997
            focus_mask None
            idle "fast_slow_button"
            action [Function(fast_pv), 
                    Hide('speed_num'), 
                    Show("speed_num")]
                
        # Slow button
        imagebutton:
            xalign 0.015
            yalign 0.997
            focus_mask None
            idle "fast_slow_button"
            action [Function(slow_pv), 
                    Hide('speed_num'), 
                    Show("speed_num")]
        

#####################################
# Chat Header Overlay
#####################################

default no_heart = False
default battery = renpy.display.behavior.pygame.power.get_power_info()
image in_chat_display = DynamicDisplayable(in_chat_fn)
default myClock = Clock(150) 

init python:
    def in_chat_fn(st, at):
        list_of_char = ''
        for index, chara in enumerate(store.in_chat):
            list_of_char += chara
            if index+1 < len(store.in_chat):
                list_of_char += ', '

        return Text(list_of_char, style='in_chat_list_style'), 0.1

    def battery_charge_icon(st, at):    
        # 0 = no idea what status is, or -1
        # 1 = running on battery, not plugged in
        # 2 = plugged in, no battery available
        # 3 = plugged in, charging
        # 4 = plugged in, battery fully charged
        battery = renpy.display.behavior.pygame.power.get_power_info()
        if battery.state == 3 or (battery.state == 4 and battery.percent <= 97):
            return Transform('battery_charged', alpha=0.75), 0.1
        elif battery.state == 4 and battery.percent > 97:
            return Transform('battery_charging', alpha=0.75), 0.1
        else:
            return Transform('transparent', size=(18,26)), 0.1

    def battery_level_bar(st, at):
        battery = renpy.display.behavior.pygame.power.get_power_info()
        if battery.percent > 50:
            img1 = "battery_high"
        elif battery.percent < 20:
            img1 = 'battery_low'
        else:
            img1 = 'battery_med'

        return Fixed(img1, Fixed('charging_icon', 
            size=(18,26), xalign=0.5, yalign=0.4)), 0.1

    def battery_empty_bar(st, at):
        battery = renpy.display.behavior.pygame.power.get_power_info()
        return Fixed("battery_empty_img", 
                Fixed('charging_icon', 
                size=(18,26), xalign=0.5, yalign=0.4)), 0.1

image battery_remaining = DynamicDisplayable(battery_level_bar)
image battery_empty = DynamicDisplayable(battery_empty_bar)
image charging_icon = DynamicDisplayable(battery_charge_icon)

style battery_bar:
    is empty
    bar_vertical True
    bottom_bar 'battery_remaining'
    top_bar 'battery_empty'
    xsize 18
    ysize 26
    align (.5, .5)

style battery_bar_undetected:
    is battery_bar
    bottom_bar "battery_high"

## This screen shows the header/footer above the chat
screen phone_overlay():  
    zorder 2
    add 'phone_ui'  # You can set this to your own image
           
    $ battery = renpy.display.behavior.pygame.power.get_power_info()

    fixed:
        xysize(150,80)
        align (0.16, 0.055)
        imagebutton:
            align (0.5, 0.5)
            focus_mask True
            idle 'max_speed_inactive'
            hover "noMaxSpeed"
            selected renpy.is_skipping()
            selected_idle 'max_speed_active'
            selected_hover "maxSpeed"
            if not choosing:
                action Skip()
                
    frame:
        align (0.75, 0.055)
        xysize (400, 80)
        add 'in_chat_display'   

    # 0 = no idea what status is, or -1
    # 1 = running on battery, not plugged in
    # 2 = plugged in, no battery available
    # 3 = plugged in, charging
    # 4 = plugged in, battery fully charged
    hbox:           
        align (1.0, 0.0)
        spacing -16
        fixed:
            xysize (20, 48)
            if battery.state >= 1 and battery.state != 2:
                bar:
                    value StaticValue(value=float(battery.percent)/100.0, 
                        range=1.0)
                    style 'battery_bar'
            else:
                bar:
                    value StaticValue(value=float(75)/100.0, 
                        range=1.0)
                    style 'battery_bar_undetected'
        add myClock xoffset 22
    
    if not starter_story:
        fixed:
            xysize (50,50)
            align (0.045, 0.065)
            imagebutton:
                align (0.5, 0.5)
                idle 'back_arrow_btn'
                hover Transform('back_arrow_btn', zoom=1.2)
                if observing or current_chatroom.expired:
                    action Jump('chat_back')
                else:
                    action Show("confirm", message="Do you really want to exit this chatroom? Please note that you cannot participate once you leave. If you want to enter this chatroom again, you will need to buy it back.", 
                                    yes_action=[Hide('confirm'), 
                                    Jump('chat_back')], 
                                    no_action=Hide('confirm'))    


#************************************
# Countdown Screen
#************************************

# This is a screen to test out timed responses
# Default countdown time is 5 seconds
screen answer_countdown(themenu, count_time=5):
    zorder 5
    timer count_time repeat False action If(persistent.autoanswer_timed_menus, 
                                
                                    [ Hide('answer_countdown'), 
                                    Hide('continue_answer_button'),
                                    Show('pause_button'),
                                    SetVariable('choosing', True),
                                    SetVariable('timed_choose', True),
                                    Jump(themenu) ],

                                    [ Hide('answer_countdown'), 
                                    Hide('continue_answer_button'), 
                                    Show('pause_button'), 
                                    SetVariable("timed_choose", False) ])

    bar value AnimatedValue(0, count_time, count_time, count_time):
        at alpha_dissolve 
        style 'answer_bar'
        

#************************************
# Continue Answer
#************************************

# Some experiments with getting the chat to continue
# while you come up with a response

default timed_choose = False
default reply_instant = False
default using_timed_menus = False

label continue_answer(themenu, count_time=5):

    # We want the timed answers to speed up/slow
    # down based on how fast the player has the
    # chat speed set to. Default is 0.8, increased/
    # decreased by 0.09 (aka increased/decreased by
    # 11.25% each time)
    python:
        modifier = 1.00
        if renpy.is_skipping():
            # Max Speed active
            modifier = 0.0
        elif pv <= 0.45:
            # speednum = "9"
            modifier = 0.1125*-4
        elif pv <= 0.54:
            # speednum = "8"
            modifier = 0.1125*-3
        elif pv <= 0.63:
            # speednum = "7"
            modifier = 0.1125*-2
        elif pv <= 0.72:
            # speednum = "6"
            modifier = 0.1125*-1
        elif pv <= 0.81:
            # speednum = "5"
            modifier = 0.00
        elif pv <= 0.90:
            # speednum = "4"
            modifier = 0.1125*1
        elif pv <= 0.99:
            # speednum = "3"
            modifier = 0.1125*2
        elif pv <= 1.08:
            # speednum = "2"
            modifier = 0.1125*3
        elif pv <= 1.17:
            # speednum = "1" 
            modifier = 0.1125*4
        else:
            # speednum = "!!"
            modifier = 0.00
        # So if the player has speed 9, which is pv=0.44 or 
        # 145% as fast as regular speed, the time should also
        # decrease by 45%
        count_time += count_time * modifier
        test_em = count_time

    # Here we make it so that timed menus don't show
    # up for players who are skipping through entire
    # conversations or who are replaying an existing
    # chatroom. Not allowing 'observing' players to 
    # choose an answer avoids the problem of players
    # who didn't initially choose an answer being unable
    # to continue
    if not renpy.is_skipping() and not observing:
        $ using_timed_menus = True
        show screen answer_countdown(themenu, count_time)
        hide screen viewCG
        $ pre_choosing = True
        show screen continue_answer_button(themenu)
    else:
        $ timed_choose = False
    return

screen continue_answer_button(themenu):
    zorder 4
    tag chat_footer
    if persistent.custom_footers:
        add "custom_answerbutton" ypos 1220
    else:
        add "answerbutton" ypos 1220
    
    imagebutton:
        ypos 1220
        focus_mask None
        idle "transparent_answer"
        activate_sound "audio/sfx/UI/answer_screen.mp3"
        action [SetVariable("choosing", True), 
                SetVariable('timed_choose', True), 
                Hide('continue_answer_button'), 
                Show('pause_button'), 
                Jump(themenu)] 
        
style answer_bar:
    bar_invert True
    thumb 'gui/slider/horizontal_idle_thumb.png'
    left_bar Frame('gui/slider/left_horizontal_bar.png',4,4)
    right_bar Frame('gui/slider/right_horizontal_bar.png',4,4)
    left_gutter 18
    right_gutter 18
    thumb_offset 18
    ypos 1210
    