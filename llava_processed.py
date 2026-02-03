
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

prompt3 = """Role: You are a specialized OCR transcription engine for comics.

Context: This is a comic strip. It consists of sub panels each with a conversation.

Dilbert is the guy wearing a red and black tie.
Dogbert is the white dog.
For any other character whose name is unknown just say unknown.

Task: Transcribe ONLY the dialogue spoken by characters panel-wise.

Rules:
Do NOT summarize the plot. If nothing is spoken in the whole image say '<No conversation>'
Do NOT describe the characters' emotions (e.g., "grumpy").
Only pick up text in speech bubbles.
Determine which character said the text by following where the tail near the text points to.

Output Format:
[Panel]
[Character]: [Text]

Image Analysis:"""

prompt4 = """You are doing STRICT COMIC TRANSCRIPTION.

Task:
Transcribe the comic strip panel by panel and assign each line to a speaker.

RULES:
1. Do NOT summarize.
2. Do NOT transcribe actions.
2. Do NOT merge panels.
3. Only say what the speaker says.
4. Preserve wording EXACTLY as written.
5. If speaker is unclear, write UNKNOWN.
6. Process panels LEFT TO RIGHT.

Dilbert is the guy wearing a red and black tie.
Dogbert is the white dog.
For any other character who is unknown just say UNKNOWN.

Output Format:
[Panel]
[Character]: [Text]

Transcription:"""

prompt5 = """You are a specialized comic transcription engine. 

**SCANNING INSTRUCTIONS:**
1. Scan the strip from left to right. 
2. Identify the vertical dividing lines (borders) between panels.
3. Every time you cross a border, start a new "PANEL [N]" block.

**IDENTIFICATION GUIDE:**
- DILBERT: Man in white shirt and red/black tie.
- DOGBERT: The small white dog.
- TRACING: There is always a little line next to the text that points to the character speaking. Carefully trace/follow the line and identify the character each time.
**OUTPUT FORMAT (STRICT):**
PANEL 1:
[Character Name]: [Text]

PANEL 2:
[Character Name]: [Text]

**STRICT RULES:**
- Do NOT output reasoning, thought tags, or summaries.
- Transcribe text verbatim.
- If a panel is empty, write "(no text)".

Remember there is a thick white region thats eperates each panel in the image.
"""

strips = load_strips("dilbert_1989_to_2023")
for strip in strips:
    print('\n\n_________________________________________\nDate:', strip['date'])
    with open("llava_processed.txt", "a", encoding="utf-8") as f:
        f.write('\n\n_________________________________________\nDate: ' + strip['date'] + '\n')
    image = strip["image"]
    panels = panelizer(strip)
    #resized_image = cv2.resize(image, None, fx=0.8, fy=0.8, interpolation=cv2.INTER_AREA)
    for i, panel in enumerate(panels):
        print("\nPanel", str(i+1) + ':')
        _, buffer = cv2.imencode(".png", image)
        response = ollama.chat(
        model='llava:13b',
        #model='llama3.2-vision',
        #model='blaifa/InternVL3_5:8b',
        options={'temperature': 0},
        messages=[{
            'role': 'user',
            'content': prompt,
            'images': [buffer.tobytes()]
        }]
        )

        print(response['message']['content'])
        with open("llava_processed.txt", "a", encoding="utf-8") as f:
            f.write('\nPanel ' + str(i+1) + ':\n' + response['message']['content'] + '\n')