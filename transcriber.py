
from loader import load_strips
from panel_splitter import panelizer
import ollama
import cv2

# Path to your panel image
image_path = '/Users/renganathc/Desktop/dilbert_strip_transcriber/dilbert_1989_to_2023/1990/1990-01-01_grumpy dog_no flattery_chocolate cake_feel better_scratch behind ears_leg spasms.gif'

prompt = """Role: You are a specialized OCR transcription engine for comics.

Context: This is a comic panel.

Dilbert is the guy wearing a red and black tie.
Dogbert is the white dog.
For any other character whose name is unknown just say unknown.

Task: Transcribe ONLY the dialogue spoken by characters.

Rules:
Do NOT summarize the plot. If nothing is spoken in the whole image say '<No conversation>'
Do NOT describe the characters' emotions (e.g., "grumpy").
Only pick up text in speech bubbles.
Determine which character said the text by following where the tail near the text points to.

Output Format:
[Character]: [Text]

Image Analysis:"""

# simpler prompt to avoid overwhelming the model
prompt2 = """Transcribe this Dilbert panel. 
Link each speech bubble to the correct character by following the tail.
Format: [Name]: [Dialogue]"""

strips = load_strips("dilbert_1989_to_2023")
for strip in strips:
    print('\n_________________________________________\nDate:', strip['date'])
    image = strip["image"]
    panels = panelizer(strip)
    for idx, panel in enumerate(panels):
        resized_image = cv2.resize(panel, None, fx=0.7, fy=0.7, interpolation=cv2.INTER_AREA)
        print('\nPanel', idx + 1)
        _, buffer = cv2.imencode(".png", resized_image)
        response = ollama.chat(
        #model='qwen2.5vl',
        #model='llama3.2-vision',
        model='blaifa/InternVL3_5:8b',
        options={'temperature': 0},
        messages=[{
            'role': 'user',
            'content': prompt,
            'images': [buffer.tobytes()]
        }]
        )

        print(response['message']['content'])