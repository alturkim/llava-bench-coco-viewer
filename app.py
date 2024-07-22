import streamlit as st
import json
import os
from PIL import Image
import json


# Load data from JSONL file
def load_data(jsonl_file):
    data = []
    with open(jsonl_file, 'r') as f:
        for line in f:
            data.append(json.loads(line.strip()))
    return data

# Group data by image
def group_data_by_image(data):
    grouped_data = {}
    for item in data:
        image = item['image']
        if image not in grouped_data:
            grouped_data[image] = []
        grouped_data[image].append(item)
    return grouped_data

# Load and group In-The-Wild data
def load_in_the_wild_data():
    questions = load_data('questions.jsonl')
    context = load_data('context.jsonl')
    answers = load_data('answers_gpt4.jsonl')
    context_dict = {item['image']: item for item in context}
    answers_dict = {item['question_id']: item for item in answers}
    
    grouped_data = {}
    for item in questions:
        image = item['image']
        if image not in grouped_data:
            grouped_data[image] = []
        question_id = item['question_id']
        caption = context_dict.get(item['image'], {}).get('caption', 'No caption available')
        answer = answers_dict.get(question_id, {}).get('text', 'No answer available')
        item['caption'] = caption
        item['answer'] = answer
        grouped_data[image].append(item)
    return grouped_data

# Main function to run the app
def main():
    # Title of the app
    st.title('Instruction-Image Viewer for LLaVA Bench')

    # Select mode
    mode = st.selectbox('Select Bench', ['COCO', 'In-The-Wild'])

    if mode == 'COCO':
        # Load data
        data = load_data('coco2014_val_gpt4_qa_30x3_ar2.jsonl')

        # Group data by image
        grouped_data = group_data_by_image(data)

        # Create a list of image filenames for the selectbox
        image_files = list(grouped_data.keys())
        
        # Create a selectbox for selecting an image
        selected_image = st.selectbox('Select an image', image_files)
        
        # Find the selected image data
        selected_data = grouped_data[selected_image]
        
        # Display the image
        img_path = os.path.join('coco_imgs', selected_image)
        image = Image.open(img_path)
        st.image(image, caption=selected_image, use_column_width=True)
        
        # Display the metadata for each set
        for item in selected_data:
            st.write('**Instruction:**', item['instruction'])
            st.write('**Output:**', item['output'])
            st.write('**Type:**', item['type'])
            st.markdown('---')

    elif mode == 'In-The-Wild':
        # Load and group data
        grouped_data = load_in_the_wild_data()

        # Create a list of image filenames for the selectbox
        image_files = list(grouped_data.keys())

        # Create a selectbox for selecting an image
        selected_image = st.selectbox('Select an image', image_files)

        # Find the selected image data
        selected_data = grouped_data[selected_image]

        # Display the image
        img_path = os.path.join('wild_imgs', selected_image)
        image = Image.open(img_path)
        st.image(image, caption=selected_image, use_column_width=True)

        # Display the metadata for each set
        for item in selected_data:
            st.write('**Category:**', item['category'])
            st.write('**Caption:**', item['caption'])
            st.write('**Question Text:**', item['text'])
            st.write('**Answer:**', item['answer'])
            st.markdown('---')

if __name__ == '__main__':
    main()
