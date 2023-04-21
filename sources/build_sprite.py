import json
from PIL import Image
from math import floor

def main():
    sprite_map = json.load(open("sprite_map.json"))

    sprite_map = sprite_map["1x"]
    sprite_map = update_relative_values(sprite_map)


    canvas_size = get_cavas_size(sprite_map)
    canvas = Image.new("RGBA", canvas_size)

    for sprite in sprite_map:
        print(sprite["name"], f"({sprite['x']},{sprite['y']},{sprite['width']},{sprite['height']})")
        y_offset = 0
        x_offset = 0
        image = Image.open("assets/"+sprite["file_name"])
        print("> source image:", f"({image.width},{image.height})")
        new_width = image.width
        if image.width > sprite["width"] or image.height > sprite["height"]:
            if image.width/sprite["width"] < image.height/sprite["height"]:
                ratio = image.height/sprite["height"]
            else:
                ratio = image.width/sprite["width"]
            new_width = int(image.width/ratio)
            new_height = int(image.height/ratio)
            print("> resizing to:", f"({new_width},{new_height}) {ratio}")
            image = image.resize((new_width, new_height), Image.Resampling.BICUBIC)

            if sprite.get("v-align","") == "bottom":
                y_offset = sprite["height"] - new_height
        if sprite.get("align","") == "center":
            x_offset = (sprite["width"]-new_width)//2


        canvas.paste(image, (sprite["x"]+x_offset,sprite["y"]+y_offset))

    canvas.save("../docs/100-offline-sprite.png","png")

def update_relative_values(sprite_map):
    previous_box = None
    for sprite in sprite_map:
        if sprite["x"] == "+":
            sprite["x"] = previous_box["x"] + previous_box["width"]
        elif sprite["x"] == "*":
            sprite["x"] = previous_box["x"]
        if sprite["y"] == "+":
            sprite["y"] = previous_box["y"] + previous_box["height"]
        elif sprite["y"] == "*":
            sprite["y"] = previous_box["y"]       
        if sprite["width"] == "*":    
            sprite["width"] = previous_box["width"] 
        if sprite["height"] == "*":    
            sprite["height"] = previous_box["height"] 

        previous_box = {"x":sprite["x"],"y":sprite["y"],"width":sprite["width"],"height":sprite["height"]}
    return sprite_map

def get_cavas_size(sprite_map):
    x_max = 0
    y_max = 0
    for sprite in sprite_map:
        x_max = max(x_max,sprite["x"]+sprite["width"])
        y_max = max(y_max,sprite["y"]+sprite["height"])

    return (x_max,y_max)

if __name__ == "__main__": main()