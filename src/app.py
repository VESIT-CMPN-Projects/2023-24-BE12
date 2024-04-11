from flask import Flask, request, jsonify, send_file
import langchain_openai
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from flask import Flask, request, jsonify
from flask_cors import CORS 
import json
import requests
import io
import base64
from PIL import Image
from io import BytesIO
import cv2
import numpy as np

def is_red_or_green(pixel):
    # Red or green in RGB. This function may need adjustment based on how you define red or green.
    return (pixel[2] > 128 and pixel[1] < 128 and pixel[0] < 128) or (pixel[1] > 128 and pixel[2] < 128 and pixel[0] < 128)

def add_text(image, text, region_coords):
    # Extract the corner coordinates of the region
    x1, y1, x2, y2 = region_coords

    # Define some parameters
    text_offset_x = 10
    text_offset_y = 30
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_color = (255, 255, 255)  # White color
    thickness = 2

    # Iterate over each word in the text and wrap it if it overflows the region
    words = text.split()
    lines = []
    line = ""
    for word in words:
        test_line = line + word + " "
        # Check if adding this word exceeds the width of the region
        (text_width, text_height), _ = cv2.getTextSize(test_line, font, font_scale, thickness)
        if text_width > (x2 - x1 - 2 * text_offset_x):  # 2 * text_offset_x for padding on both sides
            lines.append(line.strip())
            line = word + " "
        else:
            line = test_line
    lines.append(line.strip())

    # If text overflows, reduce font size
    if len(lines) * text_height > (y2 - y1 - 2 * text_offset_y):  # 2 * text_offset_y for padding on both sides
        font_scale = (y2 - y1 - 2 * text_offset_y) / (len(lines) * text_height) * font_scale

    # Write each line of text to the image
    y = y1 + text_offset_y
    for line in lines:
        # Get the size of the line
        (text_width, text_height), _ = cv2.getTextSize(line, font, font_scale, thickness)
        # Calculate the x-coordinate to center the text horizontally
        x = x1 + (x2 - x1 - text_width) // 2
        # Write the text
        cv2.putText(image, line, (x, y), font, font_scale, font_color, thickness)
        # Move to the next line
        y += int(text_height * 1.5)  # Add some space between lines

    return image


# def decode_base64_to_image(encoding):
#     if encoding.startswith("data:image/"):
#         encoding=encoding.split(";")[1].split(",")[1]
#     image=Image.open(io.BytesIO(base64.b64decode(encoding)))
#     return image

# def encode_pil_to_base64(image):
#     with io.BytesIO() as output_bytes:
#         image.save(output_bytes, format="PNG")
#         bytes_data=output_bytes.getvalue()
#     return base64.b64encode(bytes_data).decode("utf-8")

app = Flask(__name__)
CORS(app, resources={
    r"/run_script_tagline": {"origins": "http://localhost:3000"},
    r"/run_script_prompt_maker": {"origins": "http://localhost:3000"},
    r"/run_script_image": {"origins": "http://localhost:3000"},
    r"/run_merge": {"origins": "http://localhost:3000"},
})

@app.route('/run_script_tagline', methods=['POST'])
def run_script_tagline():
    # Get input data from the request sent by the React app
    data = request.get_json()
    print('Received data from React:', data)
    openai_api_key="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"
    llm=langchain_openai.OpenAI(temperature=0.7,openai_api_key=openai_api_key)
    prompt_template_name=PromptTemplate(
      input_variables=['data'],
      template="This is the product description of a product water bottle with the brand name 'AquaPure': {data} .Give me a promotional product tagline"
    )
    name_chain=LLMChain(llm=llm, prompt=prompt_template_name)
    response=name_chain({'data': data})
    print('Sending response to React:', response['text'].replace("\"",''))
    return jsonify(response['text'].replace("\"",''))

@app.route('/run_script_prompt_maker', methods=['POST'])
def run_script_prompt_maker():
    # Get input data from the request sent by the React app
    data = request.get_json()
    print('Received data from React:', data)
    openai_api_key="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"
    llm=langchain_openai.llms.OpenAI(temperature=0.7,openai_api_key=openai_api_key)
    prompt_template_name=PromptTemplate(
      input_variables=['data'],
      template= """learn from this data: [convert the  design friendly image generation prompt to image caption format. this is the prompt: Design an image for our 'Soap Bar' with 'rectangular white box' and 'go fresh' green text", this is what i want: "Women's white soap bar, white rectangular soap box, front-facing, at an angle such that the left edge of the soap box is prominently visible, blue color gradient box covering the right side of the soap box fully, picture of a stream of light blue color cream flowing into a puddle of light blue color cream is placed at the left side of the soap box on top of the gradient box, 'beauty' below which 'cream bar' dark blue color text written below the logo, clip-art of a white color drop with golden border inside which '1/4' dark blue color text is written and beside the drop is 'moisturizing cream' white color text is written, white plain background"]
[convert the  design friendly image generation prompt to image caption format. this is the prompt: Create an image for our 'Purely Pampering Shea & Vanilla' soap bar with '6 Bars' written on the box", this is what i want: "Women's white soap bar, white rectangular soap box, picture of an oval-shaped white soap bar with a dove bird engraving on it at the center on the right side of the soap box, 'white/blanc' dark blue text written below the logo, at the bottom left of the white box is a small long blue box with 'beauty bar' white text on it, golden box with a clip-art of a golden color drop, 'moisturising cream' written on the golden box, clip-art of a golden circle with a golden drop in the middle at the top right corner of the white box, white plain background"]
[convert the  design friendly image generation prompt to image caption format. this is the prompt: Design an ad image for our 'Coconut Milk' body wash bottle with a golden lid", this is what i want: "Light green cylindrical bottle, white cap lid, 'DOVE + REAL' logo, 'BIO= MIMETIC CARE' text in green color, coconut clip-art, 'REVITALISE COCONUT + VEGAN' text in white color, dark green background, 'SILICONE-FREE CONDITIONER,' 'RAEVITALISANT SANS SILICONE' text in white color, gold background, '100%' clip-art, '10 US FL OZ/295ml' text in black color, white background, 3x power, black shady label"]
[convert the  design friendly image generation prompt to image caption format. this is the prompt: Create an image for our 'Light Purple Soap Bar' with '6 Bars' written on the box", this is what i want: "Women's light purple soap bar, white rectangular soap box, small purple color box with '6 BARS' white color text written on it at the top right corner of the soap box, 'relaxing' below which 'lavender' purple color text written below the logo, small thick purple color box at the center of the soap box with 'beauty bar with coconut milk' below which 'and jasmine petals scent' white color text written on it, small thin golden color box with a clip-art of golden color drop with white border and beside the drop 'MOISTURIZING CREAM' white color text on it, picture below purple box of a lavender stems dipped in light purple color cream, '4-NET WT/PESO NETO 3.75 OZ (106g)' black color text written at the very bottom of soap box, manufacturing details at the left face of soap box, white plain background"]
[convert the  design friendly image generation prompt to image caption format. this is the prompt: Design an image for our 'Deep Moisture' body wash bottle with a brown lid", this is what i want: "Women's white long body wash bottle, brown color lid, 'new noveau' text on red oval background below logo, 'deep' below which 'moisture' dark blue color text at the center of the bottle, dark blue color gradient box with 'nourishes the driest skin' white color text written on it, '24 hr renewing micro moisture' written in golden color at bottom of body wash bottle along with clip-art of a golden colored drop, picture of half a coconut and cocoa butter dipped in white cream at bottom center of body wash bottle, 'body wash | nettoyant corporel,' '24 hr Renouvellement MicroMoisture,' '20 US FL OZ | 591 ML' text written in grey, white plain background"]
[convert the  design friendly image generation prompt to image caption format. this is the prompt: Design an ad image for our 'Men's Care' deodorant spray bottle with a green 'Extra Fresh' text", this is what i want: "Dumbbell shape grey bottle, 'NEW,' 'NON IRRITANT + VITAMIN E' on the top, 'MEN+ care' logo, green clipart, 'EXTRA FRESH,' '72 H ODOR PROTECTION,' 'LONG LASTING CITRUS SCENT"]
[convert the  design friendly image generation prompt to image caption format. this is the prompt: Design an image for our 'Night Recovery Body Cleanser Jar' with a golden top and 'Body Love' text", this is what i want: "Women's white long body cleanser jar, golden color top on the jar, On the right side of the bottle is an open container filled with voilet-colored lotion or skin care solutio, 'body love' written at the left corner in golden below dove logo, 'night recovery' voilet color text, 'Body Polish' written grey color, 'Retinol serum' written between golden colour line in voilet text at the bottom of body cleanser bottle, 'Serum De Retinol+ exfoliate' written between golden colour line in voilet text, 'Gommage Pour le corps' written in voilet, 'For dry, worn-down skin' wriiten in voilet color, white plain background"]
[convert the  design friendly image generation prompt to image caption format. this is the prompt: Create an image for our 'Rectangular Box Soap Bar' with '8 Bar Pains' written on it", this is what i want: "Soap bar, rectangular white box, '8 bar pains' written in white color in golden color box, at the center soap in light golden color with half lily flower besides soap product, 'shea butter' written in golden color at the center, 'shea butter & vanilla scent parfum de beurre de karite et vanille' white text in golden color box at bottom, 'moisturizing cream/de creme hydratante' white color text on glossy golden color box at bottom, white background"]
[convert the  design friendly image generation prompt to image caption format. this is the prompt: Create an image for our 'Restoring Men+ Care' body wash with a dark brown gradient box", this is what i want: "Women's white long body wash bottle, brown color lid, 'new noveau' text on red oval background below logo, 'restoring' brown color text at center of bottle, brown color gradient box with 'coconut & cocoa butters' white color text written on it"]
[convert the  design friendly image generation prompt to image caption format. this is the prompt: Design an image for our '100% Recycled Bottle' with dark blue and white labels", this is what i want: "Golden circle, '100%' dark blue color bold text written inside the circle at the top center, 'RECYCLED BOTTLE' dark blue color text written below '100%' text, logo at the very bottom inside golden circle"]
[convert the  design friendly image generation prompt to image caption format. this is the prompt: Design a label for our 'Deep Moisture' shampoo bottle with a green top", this is what i want: "Women's white plain shampoo bottle, plain blue color top, text and golden colored logo, curvy design, wavy image in the center, 'oxygen,' 'moisture' text written in white, blue gradient background, 'SHAMPOO,' 'VOLUMIZES FINE HAIR' text written in white, golden gradient background, '12 US FL OZ-355 mL' text written in blue, white plain background at the bottom"]
[convert the  design friendly image generation prompt to image caption format. this is the prompt: Design an image for our 'Non-Irritant Formula' Men's deodorant spray bottle", this is what i want: "Grey color deodorant spray bottle, transparent cap, 'MEN Care logo,' 'STIMULATING' text in white color, cedarwood image in the center, 'CEDARWOOD + TONKA BEANS' bold heading and '+ PLANT-BASED MOISTURIZER' sub-heading written in white text with transparent brown background, 'DRY SPRAY' white text below, '48H ANTIPERSPIRANT' black text with white background"]
[convert the  design friendly image generation prompt to image caption format. this is the prompt: Design an ad image for our 'Shea Butter & Vanilla' soap bar with '6 BARS' written on the box", this is what i want: "Women's white soap bar, white rectangular soap box, picture of an oval-shaped white soap bar dipped in white cream with an engraving of a dove bird at the left side of the soap box, 'cream beauty bar' dark blue text written below the logo, small dark blue color box at bottom left corner of soap box with 'for soft, smooth skin' white color text written on it, small golden box below dark blue box with a clip-art of golden drop with white border and beside the drop 'MOISTURIZING CREAM' white color text written on it, white plain background"]
[convert the  design friendly image generation prompt to image caption format. this is the prompt: Create an image for our 'Coconut & Vanilla' soap bar with '5 Bars' written on the box", this is what i want: "Women's white soap bar, white rectangular soap box, front-facing, at an angle such that the left edge of the soap box is prominently visible, blue color gradient box covering the right side of the soap box fully, picture of a stream of light blue color cream flowing into a puddle of light blue color cream is placed at the left side of the soap box on top of the gradient box, 'beauty' below which 'cream bar' dark blue color text written below the logo, clip-art of a white color drop with golden border inside which '1/4' dark blue color text is written and beside the drop is 'moisturizing cream' white color text is written, white plain background"]
[convert the  design friendly image generation prompt to image caption format. this is the prompt: Design an image for our 'Body Love Night Recovery' body cleanser jar with a golden top", this is what i want: "Women's white long body cleanser jar, golden color top on the jar, on the right side of the bottle is an open container filled with violet-colored lotion or skin care solution, 'body love' written at the left corner in golden below dove logo, 'night recovery' violet color text, 'Body Polish' written gray color, 'Retinol serum' written between golden color line in violet text at the bottom of the body cleanser bottle, 'Serum De Retinol+ exfoliate' written between golden color line in violet text, 'Gommage Pour le corps' written in violet, 'For dry, worn-down skin' written in violet color, white plain background"]
[convert the  design friendly image generation prompt to image caption format. this is the prompt: Create an ad image for our 'Men's Care' deodorant spray bottle with a cedarwood image", this is what i want: "Grey color deodorant spray bottle, transparent cap, 'MEN Care logo,' 'STIMULATING' text in white color, cedarwood image in the center, 'CEDARWOOD + TONKA BEANS' bold heading and '+ PLANT-BASED MOISTURIZER' sub-heading written in white text with transparent brown background, 'DRY SPRAY' white text below, '48H ANTIPERSPIRANT' black text with white background"]
[convert the  design friendly image generation prompt to image caption format. this is the prompt: Design a label for our 'Deep Moisture' shampoo bottle with a golden circle", this is what i want: "Golden circle, '100%' dark blue color bold text written inside the circle at the top center, 'RECYCLED BOTTLE' dark blue color text written below '100%' text, logo at the very bottom inside the golden circle"]
[convert the  design friendly image generation prompt to image caption format. this is the prompt: Design an image for our 'Coconut & Cocoa Butters' body wash bottle with a golden logo", this is what i want: "Light green cylindrical bottle, white cap lid, 'DOVE + REAL' logo, 'BIO= MIMETIC CARE' text in green color, coconut clip-art, 'REVITALISE COCONUT+VEGAN' text in white color, dark green background, 'SILICONE-FREE CONDITIONER,' 'RAEVITALISANT SANS SILICONE' text in white color, gold background, '100%' clip-art, '10 US FL OZ/295ml' text in black color, white background, 3x power, black shady label"]
[convert the  design friendly image generation prompt to image caption format. this is the prompt: Design an ad image for our 'Revitalisant Sans Silicone' shampoo bottle with a coconut image", this is what i want: "Light green cylindrical bottle, white cap lid, 'DOVE + REAL' logo, 'BIO= MIMETIC CARE' text in green color, coconut clip-art, 'REVITALISE COCONUT + VEGAN' text in white color, dark green background, 'SILICONE-FREE CONDITIONER,' 'RAEVITALISANT SANS SILICONE' text in white color, gold background, '100%' clip-art, '10 US FL OZ/295ml' text in black color, white background, 3x power, black shady label"]
[convert the  design friendly image generation prompt to image caption format. this is the prompt: Design an image for our '100% Recycled Bottle' with a 'Recycled Bottle' logo", this is what i want: "Golden circle, '100%' dark blue color bold text written inside the circle at the top center, 'RECYCLED BOTTLE' dark blue color text written below '100%' text, logo at the very bottom inside the golden circle"]
[convert the  design friendly image generation prompt to image caption format. this is the prompt: Design a label for our 'Endless Waves' shampoo bottle with a golden logo", this is what i want: "Women's white plain shampoo bottle, plain white color top, text and golden colored logo, curvy design, wavy image in the center, 'endless,' 'waves' text written in white, gold gradient background, 'CONDITIONER REVITALISANT' text written in white, pink gradient background, 'defines wavy hair,' 'définit les cheveux ondulés' text written in white, pink gradient background, '12 US FL OZ-355 mL' text written in blue, white plain background"]

convert this product ad image generation prompt : {data} to the "completion" format in the data. Add the relevant details. Give only completion as response."""
    )
    name_chain=LLMChain(llm=llm, prompt=prompt_template_name)
    response=name_chain({'data': data})
    print('Sending response to React:', response['text'].replace("\"",''))
    return jsonify(response['text'].replace("\"",''))


@app.route('/run_script_image', methods=['POST'])
def run_script_image():
    # Get input data from the request sent by the React app
    data = request.get_json()
    print('Received data from React:', data)
    url = "https://cdc5-3-20-229-229.ngrok-free.app/sdapi/v1/txt2img"
    data_str = "<lora:aq_train_7:2>" +"glxbtz" +str(data.get("data"))
    print(data_str)
    # controlnet_image=Image.open(r"C:\\Program Files\\GitHub\\adgenai\\src\\masks\\mask (1).png")
    # controlnet_image_data=encode_pil_to_base64(controlnet_image)
    payload = {
        "prompt": data_str,
        "sampler_name": "Euler a",
        "batch_size":4 ,
        "steps": 20,
        "cfg_scale": 7,
        "width": 512,
        "height": 512,
    }

    response = requests.post(url=url, json=payload)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        try:
            r = response.json()
            image_data_list = r.get('images', [])
            if image_data_list:
                # Convert each image to base64
                encoded_images = []
                for image_data in image_data_list:
                    image = Image.open(io.BytesIO(base64.b64decode(image_data)))
                    buffered = io.BytesIO()
                    image.save(buffered, format="PNG")
                    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
                    encoded_images.append(img_str)
                return jsonify({'images': encoded_images})
            else:
                print("No image data found in the response.")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(response.text)

    return jsonify({'error': 'Image generation failed'})

@app.route('/run_merge', methods=['POST'])
def run_merge():
    # Check if the request contains the necessary files
    if 'generatedImage' not in request.files or 'maskImage' not in request.files:
        return jsonify({'error': 'Missing images'}), 400
    
    # Get the uploaded images
    generated_image = request.files['generatedImage']
    mask_image = request.files['maskImage']
    generated_image = cv2.imdecode(np.fromstring(generated_image.read(), np.uint8), cv2.IMREAD_COLOR)
    mask_image = cv2.imdecode(np.fromstring(mask_image.read(), np.uint8), cv2.IMREAD_COLOR)
    box_size=[]
    x_y=[]
    image = mask_image
    height, width = image.shape[:2]
    ############################################################################

    #(0,0)
    x = 5
    y = 5
    k = 5

    box_region = image[0:y, 0:x]

    while 1:
        if np.any([is_red_or_green(pixel) for row in box_region for pixel in row]):
            break
        x += 5
        y += 5
        k += 5
        if y >= height or x >= width:
            break
        box_region = image[0:y, 0:x]

    print("K is: ",k)
    x_y.append([0,0,x,y])
    box_size.append(k*k)
    print("Box dimensions (x, y):", x, ",", y)

    ###################################################################################
    #(512,0)
    x = 507
    y = 5
    k = 5

    box_region = image[0:y, x:512]

    while 1:
        if np.any([is_red_or_green(pixel) for row in box_region for pixel in row]):
            break
        x -= 5
        y += 5
        k += 5
        box_region = image[0:y, x:512]

    print("K is: ",k)
    x_y.append([x,0,512,y])
    box_size.append(k*k)
    print("Box dimensions (x, y):", x, ",", y)

    #############################################################################
    #(0,512)
    x = 5
    y = 507
    k = 5

    box_region = image[y:512, 0:x]

    while 1:
        if np.any([is_red_or_green(pixel) for row in box_region for pixel in row]):
            break
        x += 5
        y -= 5
        k += 5
        box_region = image[y:512, 0:x]

    print("K is: ",k)
    x_y.append([0,y,x,512])
    box_size.append(k*k)
    print("Box dimensions (x, y):", x, ",", y)

    #############################################################################
    #(512,512)
    x = 507
    y = 507
    k = 5

    box_region = image[y:512, x:512]

    while 1:
        if np.any([is_red_or_green(pixel) for row in box_region for pixel in row]):
            break
        x -= 5
        y -= 5
        k += 5
        box_region = image[y:512, x:512]

    print("K is: ",k)
    x_y.append([x,y,512,512])
    box_size.append(k*k)
    print("Box dimensions (x, y):", x, ",", y)

    ###################################################################

    i=box_size.index(max(box_size))
    print(x_y[i])

    region_coords = x_y[i]

    # Prepare the image for adding text
    image_with_text = generated_image

    # Define text content
    text = "Your long text here, which may overflow the region. This is just an example text."

    # Add text to the image
    image_with_text = add_text(image_with_text, text, region_coords)    
    
    retval, buffer = cv2.imencode('.jpg', image_with_text)
    generated_image_with_text_base64 = base64.b64encode(buffer).decode('utf-8')
    print(generated_image_with_text_base64)
    # Return the base64 string of the resulting image to the React app
    return jsonify({'image_with_text': generated_image_with_text_base64})

if __name__ == '__main__':
    app.run(debug=True)
