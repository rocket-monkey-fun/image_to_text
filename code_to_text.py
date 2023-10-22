import dearpygui.dearpygui as dpg
from PIL import Image, ImageDraw, ImageFont
import colors

list_file_name = []
list_luminance = []
text_to_print = []
max_luminance = 255
number_of_char = 94
single_step = max_luminance / number_of_char

def ascii_to_char(number):
    character = chr(number)
    return character  

def callback_load_file(sender, app_data):
    file_name = app_data.get("file_name")
    list_file_name.clear()
    if file_name != ".":
        list_file_name.append(file_name)
    else:
        return
    resize_image()

def callback_cancel_file(sender, app_data):
    return

def resize_image():
    with Image.open(f"{list_file_name[0]}") as image_old:
        image_resolution_old = image_old.size
        text_resolution = 65
        ratio = text_resolution / max(image_resolution_old)

        if image_resolution_old[0] > image_resolution_old[1]:
            orientation = "horizontal"
        else:
            orientation = "vertical"

        if orientation == "horizontal":
            image_new = image_old.resize((65, int(ratio * min(image_resolution_old))))
        if orientation == "vertical":
            image_new = image_old.resize((int(ratio * min(image_resolution_old)), 65))

        #image_new.show()

    get_image_luminence(image_new)
    sort_ascii_char(image_new)
  
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

    char_to_luminence(char_dict_keys, image_new)

def get_image_luminence(image_new):
    pixels = list(image_new.getdata())
    for pixel in range(0, len(pixels)):
        luminance = 0.2126 * pixels[pixel][0] + 0.7152 * pixels[pixel][1] + 0.0722 * pixels[pixel][2]
        list_luminance.append(luminance)

def char_to_luminence(char_dict_keys, image_new):
    #print(char_dict_keys)
    #print(list_luminance)
    image_resolution_new = image_new.size

    luminance_value = single_step
    step_counter = 0

    image_text = open("image_text.txt", "w")

    for row in range(0, image_resolution_new[1]):
        if row != 0:
            image_text.write("\n")
        for column in range(0, image_resolution_new[0]):
            while list_luminance[(row * image_resolution_new[0]) + column] > luminance_value and luminance_value != 254.99999999999977:
                luminance_value += single_step
                step_counter += 1
                print(luminance_value)
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

with dpg.file_dialog(directory_selector = False, show = False, callback = callback_load_file, cancel_callback = callback_cancel_file, id = "file_dialog_id", width = 500 , height = 300):
    dpg.add_file_extension("", color = colors.retro_red)
    dpg.add_file_extension("Image files (*.png *.jpg *.JPG *.jpeg){.png,.jpg,.JPG,.jpeg}")
    dpg.add_file_extension(".png", color = colors.retro_turqoise)
    dpg.add_file_extension(".jpg", color = colors.retro_beige)
    dpg.add_file_extension(".JPG", color = colors.retro_beige)
    dpg.add_file_extension(".jpeg", color = colors.retro_beige)

with dpg.theme(tag = "button_theme"):
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, colors.retro_red)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, colors.retro_orange)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, colors.retro_orange)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 40)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 40, 10)

dpg.create_viewport(title = 'Image to Text', width = 600, height = 400, small_icon = "icon.ico", large_icon = "icon.ico", resizable = False)

with dpg.window(label = "First screen", pos = (100, 100), show = True, tag = "first_screen"):
    dpg.add_button(label = "Select image file", callback = lambda: dpg.show_item("file_dialog_id"))
    dpg.bind_item_theme(dpg.last_item(), "button_theme")

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("first_screen", True)
dpg.start_dearpygui()
dpg.destroy_context()