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
    openai_api_key=""
    llm=langchain_openai.OpenAI(temperature=0.7,openai_api_key=openai_api_key)
    prompt_template_name=PromptTemplate(
      input_variables=['data'],
      template="Provide 5 short promotional taglines for a new Dove soap bar product described as follows: {data}. Return the taglines separated by commas, with no numbering or additional formatting."
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
    openai_api_key=""
    llm=langchain_openai.llms.OpenAI(temperature=0.7,openai_api_key=openai_api_key)
    prompt_template_name=PromptTemplate(
      input_variables=['data'],
      template= """learn from this data: [convert the  design friendly image generation prompt to image caption format. this is the prompt: Design an image for our 'Soap Bar' with 'rectangular white box' and 'go fresh' green text", this is what i want (completion): "Women's white soap bar, white rectangular soap box, front-facing, at an angle such that the left edge of the soap box is prominently visible, blue color gradient box covering the right side of the soap box fully, picture of a stream of light blue color cream flowing into a puddle of light blue color cream is placed at the left side of the soap box on top of the gradient box, 'beauty' below which 'cream bar' dark blue color text written below the logo, clip-art of a white color drop with golden border inside which '1/4' dark blue color text is written and beside the drop is 'moisturizing cream' white color text is written, white plain background"]
[convert the  design friendly image generation prompt to image caption format. this is the prompt: Create an image for our 'Purely Pampering Shea & Vanilla' soap bar with '6 Bars' written on the box", this is what i want (completion): "Women's white soap bar, white rectangular soap box, picture of an oval-shaped white soap bar with a dove bird engraving on it at the center on the right side of the soap box, 'white/blanc' dark blue text written below the logo, at the bottom left of the white box is a small long blue box with 'beauty bar' white text on it, golden box with a clip-art of a golden color drop, 'moisturising cream' written on the golden box, clip-art of a golden circle with a golden drop in the middle at the top right corner of the white box, white plain background"]
[convert the  design friendly image generation prompt to image caption format. this is the prompt: Create an image for our 'Light Purple Soap Bar' with '6 Bars' written on the box", this is what i want(completion): "Women's light purple soap bar, white rectangular soap box, small purple color box with '6 BARS' white color text written on it at the top right corner of the soap box, 'relaxing' below which 'lavender' purple color text written below the logo, small thick purple color box at the center of the soap box with 'beauty bar with coconut milk' below which 'and jasmine petals scent' white color text written on it, small thin golden color box with a clip-art of golden color drop with white border and beside the drop 'MOISTURIZING CREAM' white color text on it, picture below purple box of a lavender stems dipped in light purple color cream, '4-NET WT/PESO NETO 3.75 OZ (106g)' black color text written at the very bottom of soap box, manufacturing details at the left face of soap box, white plain background"]
[convert the design friendly image generation prompt to image caption format. This is the prompt: "Relaxing, Lavender and Soft Gray, Lavender Fields, Moonlight, Matte Texture, Serenity Symbol", this is what I want (completion): "Women's lavender soap bar, soft gray rectangular soap box, 'Relaxing' lavender color text below the logo, picture of lavender fields under moonlight on the front side, matte texture background, small soft gray box with 'SERENITY' and a clip-art of a crescent moon, lavender and gray color theme, 'LAVENDER ESSENCE' in soft gray text at the bottom, white plain background."]
[convert the design friendly image generation prompt to image caption format. This is the prompt: "Rejuvenating, Emerald Green and Gold, Tropical Leaves, Dewdrops, Satin Finish, Renewal Symbol", this is what I want (completion): "Women's emerald green soap bar, white rectangular soap box, 'Rejuvenating' gold color text below the logo, picture of tropical leaves with dewdrops at the right side, satin finish on the box, small gold box below with 'RENEWAL' and a clip-art of a leaf with a dewdrop, emerald green and gold theme, 'TROPICAL RENEWAL' in gold text at the bottom, white plain background."]
[convert the design friendly image generation prompt to image caption format. This is the prompt: "Harmonious, Pastel Pink and Mint Green, Flower Garden, Butterflies, Smooth Finish, Harmony Symbol", this is what I want (completion): "Women's pastel pink soap bar, mint green rectangular soap box, 'Harmonious' in pastel pink text below the logo, picture of a flower garden with butterflies on the front, smooth finish on the box, small mint green box with 'HARMONY' and a clip-art of two intertwined leaves, pastel pink and mint green theme, 'GARDEN BREEZE' in mint green text at the bottom, white plain background."]
[convert the design-friendly image generation prompt to image caption format. This is the prompt: "Coral pink and golden accents, Coconut Milk and Jasmine Petals, Refreshing and Hydrating, Plain white background, Product name with scent", this is what I want (completion): "Women's white soap bar, white rectangular soap box, 'PURELY pampering coconut milk & jasmine petals' in coral pink text below the logo, plain white background, coral pink box with golden accents at the bottom left corner, picture of coconut and jasmine petals on the right side, 'REFRESHING & HYDRATING' in golden text, white plain background."]
[convert the design-friendly image generation prompt to image caption format. This is the prompt: "Light green with green accents, Lavender and Chamomile, Calming and Relaxing, White background with texture, Additional benefits or features", this is what I want (completion): "Women's white soap bar, white rectangular soap box, 'Calming and Relaxing lavender & chamomile' in light green text, white background with a textured pattern mimicking soft fabric, small green box at the bottom right with 'BEAUTY BAR' text, 'anti-stress, fragrance free, hypoallergenic' features listed below in green accents, picture of lavender stems and chamomile flowers on the left, white plain background."]
[convert the design-friendly image generation prompt to image caption format. This is the prompt: "Light blue with blue accents, Cherry and Chia Milk, Energizing and Revitalizing, Background with a specific color related to the scent or feature, Promotional offers", this is what I want (completion): "Women's white soap bar, white rectangular soap box, 'Energizing and Revitalizing cherry & chia milk' in light blue text, background in a specific color related to cherry scent which is a soft red gradient into light blue, small blue box with 'BEAUTY BAR' text, 'Buy 4 Get 1 FREE' promotional offer in blue accents at the top right corner, picture of cherries and a splash of milk on the left, light blue and red accents, white plain background."]
[convert the design friendly image generation prompt to image caption format. this is the prompt: "Design an image for our 'Soap Bar' with 'rectangular white box' and 'go fresh' green text", this is what i want (completion): "Women's white soap bar, white rectangular soap box, front-facing angle with the left edge prominently visible, blue gradient box covering the right side, stream of light blue cream flowing into a puddle, 'beauty' and 'cream bar' in dark blue text, clip-art of a white drop with '1/4' in dark blue and 'moisturizing cream' beside it, white plain background."]
[convert the design friendly image generation prompt to image caption format. this is the prompt: "Create an image for our 'Purely Pampering Shea & Vanilla' soap bar with '6 Bars' written on the box", this is what i want (completion): "Women's white soap bar, white rectangular soap box, oval-shaped white soap bar with dove bird engraving, 'white/blanc' in dark blue text, small long blue box with 'beauty bar,' golden box with 'moisturizing cream,' clip-art of a golden circle with a drop, white plain background."]
[convert the design friendly image generation prompt to image caption format. this is the prompt: "Create an image for our 'Light Purple Soap Bar' with '6 Bars' written on the box", this is what i want (completion): "Women's light purple soap bar, white rectangular soap box, small purple box with '6 BARS' at the top right corner, 'relaxing' and 'lavender' in purple text, thick purple box with 'beauty bar with coconut milk' and 'and jasmine petals scent,' small thin golden box with a drop and 'MOISTURIZING CREAM,' lavender stems dipped in light purple cream, '4-NET WT/PESO NETO 3.75 OZ (106g)' at the bottom, white plain background."]
[convert the design friendly image generation prompt to image caption format. this is the prompt: "Exotic and Pampering, Coral Pink and Gold, Flowers and Fruits, Creamy Textures, Gradient Background, Hydration Symbol", this is what i want (completion): "Women's soap bar in coral pink and gold, white rectangular soap box with gradient background, images of flowers and fruits with creamy textures, small golden box with hydration symbol at the bottom."]
[Convert the design friendly image generation prompt to image caption format. This is the prompt: Design an image for our 'Soap Bar' with 'rectangular white box' and 'go fresh' green text, This is what I want (completion): Women's white soap bar, white rectangular soap box, front-facing, at an angle such that the left edge of the soap box is prominently visible, blue color gradient box covering the right side of the soap box fully, picture of a stream of light blue color cream flowing into a puddle of light blue color cream is placed at the left side of the soap box on top of the gradient box, 'beauty' below which 'cream bar' dark blue color text written below the logo, clip-art of a white color drop with golden border inside which '1/4' dark blue color text is written and beside the drop is 'moisturizing cream' white color text is written, white plain background]
[Convert the design friendly image generation prompt to image caption format. This is the prompt: Create an image for our 'Purely Pampering Shea & Vanilla' soap bar with '6 Bars' written on the box, This is what I want (completion): Women's white soap bar, white rectangular soap box, picture of an oval-shaped white soap bar with a dove bird engraving on it at the center on the right side of the soap box, 'white/blanc' dark blue text written below the logo, at the bottom left of the white box is a small long blue box with 'beauty bar' white text on it, golden box with a clip-art of a golden color drop, 'moisturising cream' written on the golden box, clip-art of a golden circle with a golden drop in the middle at the top right corner of the white box, white plain background]
[Convert the design friendly image generation prompt to image caption format. This is the prompt: Create an image for our 'Light Purple Soap Bar' with '6 Bars' written on the box, This is what I want (completion): Women's light purple soap bar, white rectangular soap box, small purple color box with '6 BARS' white color text written on it at the top right corner of the soap box, 'relaxing' below which 'lavender' purple color text written below the logo, small thick purple color box at the center of the soap box with 'beauty bar with coconut milk' below which 'and jasmine petals scent' white color text written on it, small thin golden color box with a clip-art of golden color drop with white border and beside the drop 'MOISTURIZING CREAM' white color text on it, picture below purple box of a lavender stems dipped in light purple color cream, '4-NET WT/PESO NETO 3.75 OZ (106g)' black color text written at the very bottom of soap box, manufacturing details at the left face of soap box, white plain background]
[Convert the design friendly image generation prompt to image caption format. This is the prompt: Design an image for our 'Fresh Citrus' soap bar with '4 Bars' written on the box, This is what I want (completion): Women's white soap bar, white rectangular soap box, front-facing, tilted such that the left edge of the soap box is prominently visible, citrus fruits illustration covering the background, 'Fresh Citrus' green text written below the logo, small thick orange color box at the center of the soap box with 'beauty bar with citrus essence' below which 'invigorating and refreshing' white color text written on it, small thin golden color box with a clip-art of a golden color drop with white border and beside the drop 'MOISTURIZING CREAM' white color text on it, picture at the right side of soap box of citrus slices and leaves dipped in white color cream, '4-NET WT/PESO NETO 3.75 OZ (106g)' black color text written at the very bottom of soap box, white plain background]
[Convert the design friendly image generation prompt to image caption format. This is the prompt: Create an image for our 'Soothing Aloe Vera' soap bar with 'Limited Edition' written on the box, This is what I want(completion): Women's light green soap bar, white rectangular soap box, front-facing, at an angle such that the top edge of the soap box is prominently visible, aloe vera plant illustration covering the background, 'Soothing Aloe Vera' blue text written below the logo, small thick light blue color box at the center of the soap box with 'beauty bar with aloe vera extract' below which 'calming and moisturizing' white color text written on it, small thin golden color box with a clip-art of a golden color drop with white border and beside the drop 'MOISTURIZING CREAM' white color text on it, picture at the left side of soap box of aloe vera leaves dipped in light green color cream, 'Limited Edition' red color text written at the bottom right corner of soap box, white plain background]
[Convert the design friendly image generation prompt to image caption format. This is the prompt: Design an image for our 'Exfoliating Coffee Scrub' soap bar with '100% Natural' written on the box, This is what I want(completion): Women's brown soap bar, white rectangular soap box, front-facing, tilted such that the right edge of the soap box is prominently visible, coffee beans illustration covering the background, 'Exfoliating Coffee Scrub' black text written below the logo, small thick brown color box at the center of the soap box with 'beauty bar with coffee grounds' below which 'invigorating and exfoliating' white color text written on it, small thin golden color box with a clip-art of a golden color drop with white border and beside the drop 'MOISTURIZING CREAM' white color text on it, picture at the left side of soap box of coffee beans dipped in brown color cream, '100% Natural' green color text written at the bottom right corner of soap box, white plain background]
[Convert the design friendly image generation prompt to image caption format. This is the prompt: Create an image for our 'Gentle Baby Soap' with 'Hypoallergenic' written on the box, This is what I want (completion): Women's light blue soap bar, white rectangular soap box, front-facing, tilted such that the left edge of the soap box is prominently visible, baby illustration covering the background, 'Gentle Baby Soap' pink text written below the logo, small thick pink color box at the center of the soap box with 'hypoallergenic formula' below which 'gentle and nourishing' white color text written on it, small thin golden color box with a clip-art of a golden color drop with white border and beside the drop 'MOISTURIZING CREAM' white color text on it, picture at the right side of soap box of baby booties dipped in light blue color cream, 'Hypoallergenic' blue color text written at the bottom right corner of soap box, white plain background]

convert this product ad image generation prompt : {data} to the "completion" format in the data. Add the relevant details. Give only completion as response."""
    )
    name_chain=LLMChain(llm=llm, prompt=prompt_template_name)
    response=name_chain({'data': data})
    completion_response = response['text'].replace("\"", '')
    if "(completion):" in completion_response:
        # Extract only the completion part
        completion_response = completion_response.split("(completion): ")[1]
    print('Sending response to React:', completion_response)
    return jsonify(completion_response)


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
