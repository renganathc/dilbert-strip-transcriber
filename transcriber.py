
from loader import load_strips
from panel_splitter import panelizer
import ollama
import cv2

# Path to your panel image
image_path = '/Users/renganathc/Desktop/dilbert_strip_transcriber/dilbert_1989_to_2023/1990/1990-01-01_grumpy dog_no flattery_chocolate cake_feel better_scratch behind ears_leg spasms.gif'

prompt = """Role: You are a specialized OCR transcription engine for comics.

Context: This is a comic panel.

Dilbert: Guy wearing a red and black tie.
Dogbert: The white dog.
Other: Any other character

Task: Transcribe ONLY the dialogue spoken by characters.

Rules:
Do NOT summarize the plot.
Do NOT describe the characters' emotions (e.g., "grumpy").
Only pick up text in speech bubbles.
Determine which character said the text by following where the tail near the text points to.

Output Format:
[Character]: [Text]

Image Analysis:"""

strips = load_strips("dilbert_1989_to_2023")
for strip in strips:
    image = strip["image"]
    panels = panelizer(strip)
    for image in panels:
        _, buffer = cv2.imencode(".png", image)
        response = ollama.chat(
        model='qwen2.5vl',
        #model='llama3.2-vision',
        options={'temperature': 0},
        messages=[{
            'role': 'user',
            'content': prompt,
            'images': [buffer.tobytes()]
        }]
        )

        print(response['message']['content'])