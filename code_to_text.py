import dearpygui.dearpygui as dpg
from PIL import Image, ImageDraw, ImageFont
import colors
import os
import time

list_file_path_name_load = []
list_file_path_name_save = []
list_luminance = []
text_to_print = []
error = []
max_luminance = 255
number_of_char = 94
single_step = max_luminance / number_of_char

def ascii_to_char(number):
    character = chr(number)
    return character  

def callback_load_file(sender, app_data):
    file_path_name_load = app_data.get("file_path_name")
    list_file_path_name_load.append(file_path_name_load)
    file_name_load = app_data.get("file_name")

    dpg.set_value("load_text", file_name_load)
    dpg.configure_item("file_load_button", enabled = False)
    dpg.bind_item_theme("file_load_button", "button_theme_disabled")
    dpg.configure_item("file_save_button", show = True)
    dpg.configure_item("save_text", show = True)

def callback_save_file(sender, app_data):
    file_path_name_save = app_data.get("file_path_name")
    list_file_path_name_save.append(file_path_name_save)
    file_name_save = app_data.get("file_name")

    dpg.set_value("save_text", file_name_save)
    dpg.configure_item("file_save_button", enabled = False)
    dpg.bind_item_theme("file_save_button", "button_theme_disabled")

    dpg.configure_item("create_button", show = True)
    dpg.configure_item("create_text", show = True)

def callback_create():
    dpg.configure_item("create_button", enabled = False)
    dpg.bind_item_theme("create_button", "button_theme_disabled")
    resize_image()
    if len(error) == 0:
        time.sleep(1.5)
        dpg.set_value("create_text", "Done!")

    dpg.configure_item("close_button", show = True)

def callback_close():
    os._exit(0)

def callback_cancel_file(sender, app_data):
    return

def resize_image():
    try:
        with Image.open(f"{list_file_path_name_load[0]}") as image_old:
            image_resolution_old = image_old.size
            text_resolution = 105
            ratio = text_resolution / max(image_resolution_old)

            if image_resolution_old[0] > image_resolution_old[1]:
                orientation = "horizontal"
            else:
                orientation = "vertical"

            if orientation == "horizontal":
                image_new = image_old.resize((text_resolution, int(ratio * min(image_resolution_old))))
            if orientation == "vertical":
                image_new = image_old.resize((int(ratio * min(image_resolution_old)), text_resolution))

            #image_new.show()

        get_image_luminence(image_new)
        sort_ascii_char(image_new)
    except FileNotFoundError:
        error.append(1)
        dpg.set_value("create_text", "Image not found!")
  
def sort_ascii_char(image_new):    
    menlo = ImageFont.truetype('Menlo.ttc', 100)
    char_dict = {}
    for i in range(33, 127): #33, 127
        testimage = Image.new('1', (150, 150))
        draw = ImageDraw.Draw(testimage)
        draw.text((0, 0), ascii_to_char(i) , font = menlo, fill = "#FFFFFF")
        
        #testimage.show()
        #testimage.save(f"imgs/{i}_char.png")
        
        pixels = list(testimage.getdata())
        white_pixel_count = pixels.count(255)
        char_dict[i] = white_pixel_count
    
    # sorted tuple list by luminance
    sorted_char_dict = sorted(char_dict.items(), key = lambda x:x[1])
    # tuple list to dictionary
    converted_char_dict = dict(sorted_char_dict)
    # list of dictionary keys
    char_dict_keys = list(converted_char_dict.keys())

    luminence_to_char(char_dict_keys, image_new)

def get_image_luminence(image_new):
    pixels = list(image_new.getdata())
    for pixel in range(0, len(pixels)):
        luminance = 0.2126 * pixels[pixel][0] + 0.7152 * pixels[pixel][1] + 0.0722 * pixels[pixel][2]
        list_luminance.append(luminance)

def luminence_to_char(char_dict_keys, image_new):
    #print(char_dict_keys)
    #print(list_luminance)
    image_resolution_new = image_new.size
    print(image_resolution_new)

    luminance_value = single_step
    step_counter = 0

    image_text = open(f"{list_file_path_name_save[0]}", "w")

    for row in range(0, image_resolution_new[1]):
        if row != 0:
            image_text.write("\n")
        for column in range(0, image_resolution_new[0]):
            while list_luminance[(row * image_resolution_new[0]) + column] > luminance_value and luminance_value != 254.99999999999977:
                luminance_value += single_step
                step_counter += 1
                #print(luminance_value)
            else:
                char_to_print = char_dict_keys[step_counter]
                image_text.write(ascii_to_char(char_to_print))
                image_text.write(ascii_to_char(char_to_print))
                luminance_value = single_step
                step_counter = 0

# write ascii characters into .txt file
# ascii_num_to_char = open("ascii_num_to_char.txt", "w")
# for i in range(33, 127):
#    ascii_num_to_char.write(str(i))
#    ascii_num_to_char.write(" = ")
#    ascii_num_to_char.write(ascii_to_char(i))
#    ascii_num_to_char.write("\n")

##########################################################################################################################################################################

dpg.create_context()

with dpg.file_dialog(directory_selector = False, show = False, callback = callback_load_file, cancel_callback = callback_cancel_file, default_filename = "", id = "file_dialog_load", width = 500 , height = 300):
    dpg.add_file_extension("", color = colors.retro_red)
    dpg.add_file_extension("Image files (*.png *.jpg *.jpeg){.png,.jpg,.jpeg}")
    dpg.add_file_extension(".png", color = colors.retro_turqoise)
    dpg.add_file_extension(".jpg", color = colors.retro_beige)
    dpg.add_file_extension(".jpeg", color = colors.retro_beige)

with dpg.file_dialog(directory_selector = False, show = False, callback = callback_save_file, cancel_callback = callback_cancel_file, default_filename = "", id = "file_dialog_save", width = 500 , height = 300):
    dpg.add_file_extension("", color = colors.retro_red)
    dpg.add_file_extension(".txt", color = colors.retro_turqoise)

with dpg.theme(tag = "button_theme_enabled"):
    with dpg.theme_component(dpg.mvButton, enabled_state = True):
        dpg.add_theme_color(dpg.mvThemeCol_Button, colors.retro_red)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, colors.retro_orange)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, colors.retro_orange)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 40)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 40, 10)

with dpg.theme(tag = "button_theme_disabled"):
    with dpg.theme_component(dpg.mvButton, enabled_state = False):
        dpg.add_theme_color(dpg.mvThemeCol_Button, colors.retro_red)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, colors.retro_red)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, colors.retro_red)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 40)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 40, 10)

dpg.create_viewport(title = 'Image to Text', width = 600, height = 400, small_icon = "icon.ico", large_icon = "icon.ico", resizable = False)

with dpg.window(label = "First screen", pos = (100, 100), show = True, tag = "first_screen"):
    with dpg.group(horizontal = True):
        dpg.add_button(label = "  Load image  ", callback = lambda: dpg.show_item("file_dialog_load"), tag = "file_load_button")
        dpg.bind_item_theme("file_load_button", "button_theme_enabled")
        dpg.add_text("Selected image...", tag = "load_text")

    with dpg.group(horizontal = True):
        dpg.add_button(label = "Save textimage", show = False, callback = lambda: dpg.show_item("file_dialog_save"), tag = "file_save_button")
        dpg.bind_item_theme("file_save_button", "button_theme_enabled")
        dpg.add_text("Selected textimage...", show = False, tag = "save_text")

    with dpg.group(horizontal = True):
        dpg.add_button(label = "    Create    ", show = False, callback = callback_create, tag = "create_button")
        dpg.bind_item_theme("create_button", "button_theme_enabled")
        dpg.add_text("Wait...", show = False, tag = "create_text")

    dpg.add_button(label = "    Close    ", show = False, callback = callback_close, tag = "close_button")
    dpg.bind_item_theme("close_button", "button_theme_enabled")

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("first_screen", True)
dpg.start_dearpygui()
dpg.destroy_context()