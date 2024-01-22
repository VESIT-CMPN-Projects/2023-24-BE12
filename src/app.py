from flask import Flask, request, jsonify
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


app = Flask(__name__)
CORS(app, resources={r"/run_script_tagline": {"origins": "http://localhost:3000"}, r"/run_script_prompt_maker": {"origins": "http://localhost:3000"}, r"/run_script_image": {"origins": "http://localhost:3000"}})

@app.route('/run_script_tagline', methods=['POST'])
def run_script_tagline():
    # Get input data from the request sent by the React app
    data = request.get_json()
    print('Received data from React:', data)
    openai_api_key="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"
    llm=langchain_openai.OpenAI(temperature=0.7,openai_api_key=openai_api_key)
    prompt_template_name=PromptTemplate(
      input_variables=['data'],
      template="This is the product description of a new Dove product: {data} .Give me a new promotional product tagline that is similar to what Dove uses as product taglines"
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
      template= """learn from this data: ["prompt": "convert the  design friendly image generation prompt to image caption format. this is the prompt: Design an image for our 'Soap Bar' with 'rectangular white box' and 'go fresh' green text", "completion": "Women's white soap bar, white rectangular soap box, front-facing, at an angle such that the left edge of the soap box is prominently visible, blue color gradient box covering the right side of the soap box fully, picture of a stream of light blue color cream flowing into a puddle of light blue color cream is placed at the left side of the soap box on top of the gradient box, 'beauty' below which 'cream bar' dark blue color text written below the logo, clip-art of a white color drop with golden border inside which '1/4' dark blue color text is written and beside the drop is 'moisturizing cream' white color text is written, white plain background"]
["prompt": "convert the  design friendly image generation prompt to image caption format. this is the prompt: Create an image for our 'Purely Pampering Shea & Vanilla' soap bar with '6 Bars' written on the box", "completion": "Women's white soap bar, white rectangular soap box, picture of an oval-shaped white soap bar with a dove bird engraving on it at the center on the right side of the soap box, 'white/blanc' dark blue text written below the logo, at the bottom left of the white box is a small long blue box with 'beauty bar' white text on it, golden box with a clip-art of a golden color drop, 'moisturising cream' written on the golden box, clip-art of a golden circle with a golden drop in the middle at the top right corner of the white box, white plain background"]
["prompt": "convert the  design friendly image generation prompt to image caption format. this is the prompt: Design an ad image for our 'Coconut Milk' body wash bottle with a golden lid", "completion": "Light green cylindrical bottle, white cap lid, 'DOVE + REAL' logo, 'BIO= MIMETIC CARE' text in green color, coconut clip-art, 'REVITALISE COCONUT + VEGAN' text in white color, dark green background, 'SILICONE-FREE CONDITIONER,' 'RAEVITALISANT SANS SILICONE' text in white color, gold background, '100%' clip-art, '10 US FL OZ/295ml' text in black color, white background, 3x power, black shady label"]
["prompt": "convert the  design friendly image generation prompt to image caption format. this is the prompt: Create an image for our 'Light Purple Soap Bar' with '6 Bars' written on the box", "completion": "Women's light purple soap bar, white rectangular soap box, small purple color box with '6 BARS' white color text written on it at the top right corner of the soap box, 'relaxing' below which 'lavender' purple color text written below the logo, small thick purple color box at the center of the soap box with 'beauty bar with coconut milk' below which 'and jasmine petals scent' white color text written on it, small thin golden color box with a clip-art of golden color drop with white border and beside the drop 'MOISTURIZING CREAM' white color text on it, picture below purple box of a lavender stems dipped in light purple color cream, '4-NET WT/PESO NETO 3.75 OZ (106g)' black color text written at the very bottom of soap box, manufacturing details at the left face of soap box, white plain background"]
["prompt": "convert the  design friendly image generation prompt to image caption format. this is the prompt: Design an image for our 'Deep Moisture' body wash bottle with a brown lid", "completion": "Women's white long body wash bottle, brown color lid, 'new noveau' text on red oval background below logo, 'deep' below which 'moisture' dark blue color text at the center of the bottle, dark blue color gradient box with 'nourishes the driest skin' white color text written on it, '24 hr renewing micro moisture' written in golden color at bottom of body wash bottle along with clip-art of a golden colored drop, picture of half a coconut and cocoa butter dipped in white cream at bottom center of body wash bottle, 'body wash | nettoyant corporel,' '24 hr Renouvellement MicroMoisture,' '20 US FL OZ | 591 ML' text written in grey, white plain background"]
["prompt": "convert the  design friendly image generation prompt to image caption format. this is the prompt: Design an ad image for our 'Men's Care' deodorant spray bottle with a green 'Extra Fresh' text", "completion": "Dumbbell shape grey bottle, 'NEW,' 'NON IRRITANT + VITAMIN E' on the top, 'MEN+ care' logo, green clipart, 'EXTRA FRESH,' '72 H ODOR PROTECTION,' 'LONG LASTING CITRUS SCENT"]
["prompt": "convert the  design friendly image generation prompt to image caption format. this is the prompt: Design an image for our 'Night Recovery Body Cleanser Jar' with a golden top and 'Body Love' text", "completion": "Women's white long body cleanser jar, golden color top on the jar, On the right side of the bottle is an open container filled with voilet-colored lotion or skin care solutio, 'body love' written at the left corner in golden below dove logo, 'night recovery' voilet color text, 'Body Polish' written grey color, 'Retinol serum' written between golden colour line in voilet text at the bottom of body cleanser bottle, 'Serum De Retinol+ exfoliate' written between golden colour line in voilet text, 'Gommage Pour le corps' written in voilet, 'For dry, worn-down skin' wriiten in voilet color, white plain background"]
["prompt": "convert the  design friendly image generation prompt to image caption format. this is the prompt: Create an image for our 'Rectangular Box Soap Bar' with '8 Bar Pains' written on it", "completion": "Soap bar, rectangular white box, '8 bar pains' written in white color in golden color box, at the center soap in light golden color with half lily flower besides soap product, 'shea butter' written in golden color at the center, 'shea butter & vanilla scent parfum de beurre de karite et vanille' white text in golden color box at bottom, 'moisturizing cream/de creme hydratante' white color text on glossy golden color box at bottom, white background"]
["prompt": "convert the  design friendly image generation prompt to image caption format. this is the prompt: Create an image for our 'Restoring Men+ Care' body wash with a dark brown gradient box", "completion": "Women's white long body wash bottle, brown color lid, 'new noveau' text on red oval background below logo, 'restoring' brown color text at center of bottle, brown color gradient box with 'coconut & cocoa butters' white color text written on it"]
["prompt": "convert the  design friendly image generation prompt to image caption format. this is the prompt: Design an image for our '100% Recycled Bottle' with dark blue and white labels", "completion": "Golden circle, '100%' dark blue color bold text written inside the circle at the top center, 'RECYCLED BOTTLE' dark blue color text written below '100%' text, logo at the very bottom inside golden circle"]
["prompt": "convert the  design friendly image generation prompt to image caption format. this is the prompt: Design a label for our 'Deep Moisture' shampoo bottle with a green top", "completion": "Women's white plain shampoo bottle, plain blue color top, text and golden colored logo, curvy design, wavy image in the center, 'oxygen,' 'moisture' text written in white, blue gradient background, 'SHAMPOO,' 'VOLUMIZES FINE HAIR' text written in white, golden gradient background, '12 US FL OZ-355 mL' text written in blue, white plain background at the bottom"]
["prompt": "convert the  design friendly image generation prompt to image caption format. this is the prompt: Design an image for our 'Non-Irritant Formula' Men's deodorant spray bottle", "completion": "Grey color deodorant spray bottle, transparent cap, 'MEN Care logo,' 'STIMULATING' text in white color, cedarwood image in the center, 'CEDARWOOD + TONKA BEANS' bold heading and '+ PLANT-BASED MOISTURIZER' sub-heading written in white text with transparent brown background, 'DRY SPRAY' white text below, '48H ANTIPERSPIRANT' black text with white background"]
["prompt": "convert the  design friendly image generation prompt to image caption format. this is the prompt: Design an ad image for our 'Shea Butter & Vanilla' soap bar with '6 BARS' written on the box", "completion": "Women's white soap bar, white rectangular soap box, picture of an oval-shaped white soap bar dipped in white cream with an engraving of a dove bird at the left side of the soap box, 'cream beauty bar' dark blue text written below the logo, small dark blue color box at bottom left corner of soap box with 'for soft, smooth skin' white color text written on it, small golden box below dark blue box with a clip-art of golden drop with white border and beside the drop 'MOISTURIZING CREAM' white color text written on it, white plain background"]
["prompt": "convert the  design friendly image generation prompt to image caption format. this is the prompt: Create an image for our 'Coconut & Vanilla' soap bar with '5 Bars' written on the box", "completion": "Women's white soap bar, white rectangular soap box, front-facing, at an angle such that the left edge of the soap box is prominently visible, blue color gradient box covering the right side of the soap box fully, picture of a stream of light blue color cream flowing into a puddle of light blue color cream is placed at the left side of the soap box on top of the gradient box, 'beauty' below which 'cream bar' dark blue color text written below the logo, clip-art of a white color drop with golden border inside which '1/4' dark blue color text is written and beside the drop is 'moisturizing cream' white color text is written, white plain background"]
["prompt": "convert the  design friendly image generation prompt to image caption format. this is the prompt: Design an image for our 'Body Love Night Recovery' body cleanser jar with a golden top", "completion": "Women's white long body cleanser jar, golden color top on the jar, on the right side of the bottle is an open container filled with violet-colored lotion or skin care solution, 'body love' written at the left corner in golden below dove logo, 'night recovery' violet color text, 'Body Polish' written gray color, 'Retinol serum' written between golden color line in violet text at the bottom of the body cleanser bottle, 'Serum De Retinol+ exfoliate' written between golden color line in violet text, 'Gommage Pour le corps' written in violet, 'For dry, worn-down skin' written in violet color, white plain background"]
["prompt": "convert the  design friendly image generation prompt to image caption format. this is the prompt: Create an ad image for our 'Men's Care' deodorant spray bottle with a cedarwood image", "completion": "Grey color deodorant spray bottle, transparent cap, 'MEN Care logo,' 'STIMULATING' text in white color, cedarwood image in the center, 'CEDARWOOD + TONKA BEANS' bold heading and '+ PLANT-BASED MOISTURIZER' sub-heading written in white text with transparent brown background, 'DRY SPRAY' white text below, '48H ANTIPERSPIRANT' black text with white background"]
["prompt": "convert the  design friendly image generation prompt to image caption format. this is the prompt: Design a label for our 'Deep Moisture' shampoo bottle with a golden circle", "completion": "Golden circle, '100%' dark blue color bold text written inside the circle at the top center, 'RECYCLED BOTTLE' dark blue color text written below '100%' text, logo at the very bottom inside the golden circle"]
["prompt": "convert the  design friendly image generation prompt to image caption format. this is the prompt: Design an image for our 'Coconut & Cocoa Butters' body wash bottle with a golden logo", "completion": "Light green cylindrical bottle, white cap lid, 'DOVE + REAL' logo, 'BIO= MIMETIC CARE' text in green color, coconut clip-art, 'REVITALISE COCONUT+VEGAN' text in white color, dark green background, 'SILICONE-FREE CONDITIONER,' 'RAEVITALISANT SANS SILICONE' text in white color, gold background, '100%' clip-art, '10 US FL OZ/295ml' text in black color, white background, 3x power, black shady label"]
["prompt": "convert the  design friendly image generation prompt to image caption format. this is the prompt: Design an ad image for our 'Revitalisant Sans Silicone' shampoo bottle with a coconut image", "completion": "Light green cylindrical bottle, white cap lid, 'DOVE + REAL' logo, 'BIO= MIMETIC CARE' text in green color, coconut clip-art, 'REVITALISE COCONUT + VEGAN' text in white color, dark green background, 'SILICONE-FREE CONDITIONER,' 'RAEVITALISANT SANS SILICONE' text in white color, gold background, '100%' clip-art, '10 US FL OZ/295ml' text in black color, white background, 3x power, black shady label"]
["prompt": "convert the  design friendly image generation prompt to image caption format. this is the prompt: Design an image for our '100% Recycled Bottle' with a 'Recycled Bottle' logo", "completion": "Golden circle, '100%' dark blue color bold text written inside the circle at the top center, 'RECYCLED BOTTLE' dark blue color text written below '100%' text, logo at the very bottom inside the golden circle"]
["prompt": "convert the  design friendly image generation prompt to image caption format. this is the prompt: Design a label for our 'Endless Waves' shampoo bottle with a golden logo", "completion": "Women's white plain shampoo bottle, plain white color top, text and golden colored logo, curvy design, wavy image in the center, 'endless,' 'waves' text written in white, gold gradient background, 'CONDITIONER REVITALISANT' text written in white, pink gradient background, 'defines wavy hair,' 'définit les cheveux ondulés' text written in white, pink gradient background, '12 US FL OZ-355 mL' text written in blue, white plain background"]

convert this product ad image generation prompt : {data} to the "completion" format in the data. Add the relevant details. Give only completion as response."""
    )
    name_chain=LLMChain(llm=llm, prompt=prompt_template_name)
    response=name_chain({'data': data})
    print('Sending response to React:', response['text'].replace("\"",''))
    return jsonify(response['text'].replace("\"",''))


@app.route('/run_script_image', methods=['POST'])
def run_script_image():
  #Get input data from the request sent by the React app
  data = request.get_json()
  print('Received data from React:', data)
  url = "https://697a-3-135-152-169.ngrok-free.app"
  endpoint = "/sdapi/v1/txt2img"
  full_url = f'{url}{endpoint}'
  data=str("<lora:dove_750_final-09:2>"+str(data))
  print(data)
  payload = {
    "prompt": data,
    "sampler_name": "DPM++ 2M Karras",
    "batch_size": 1,
    "n_iter": 1,
    "steps": 30,
    "cfg_scale": 9,
    "width": 512,
    "height": 512,
    "refiner_checkpoint": "",
    "refiner_switch_at": 0.8,
    "hr_upscaler": "Latent",
    "hr_second_pass_steps": 0,
    "sampler_index": "Euler",
  }

  response = requests.post(url=full_url, json=payload)

  # Check if the request was successful (status code 200)
  if response.status_code == 200:
        try:
            r = response.json()
            image_data = r.get('images', [])
            if image_data:
                # Assuming there's at least one image in the response
                image = Image.open(io.BytesIO(base64.b64decode(image_data[0])))
                # Convert image to base64
                buffered = io.BytesIO()
                image.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
                return jsonify({'image': img_str})
            else:
                print("No image data found in the response.")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
  else:
      print(f"Request failed with status code: {response.status_code}")
      print(response.text)

  return jsonify({'error': 'Image generation failed'})

if __name__ == '__main__':
    app.run(debug=True)
