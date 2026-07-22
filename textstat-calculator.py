from ollama import chat
from ollama import ChatResponse
import textstat
from textstat import flesch_kincaid_grade, gunning_fog, smog_index, text_standard, automated_readability_index, coleman_liau_index
import pandas as pd
import csv

#Workflow: only look at every second grade (to cut down on testing needed). Open file of texts for that level. Get first 3 rows of each grade. 
#What to record: start level, end level, distance from start to desired, distance from end to desired, distance from start to end

grades = [0, 2, 4, 6, 8, 10, 12]

model = input("What model would you like to use?")


for grade in grades:
    lines = pd.read_csv("fkgl-texts/{grade}.csv".format(grade = grade)) #open the csv with the texts for that level
    top_3 = lines.head(3) #get first 3 texts
    texts = top_3.iloc[:, 0].to_list() #transform to list
    texts_fkgl = top_3.iloc[:, 1].to_list() #transform to list

    for text_num, text in enumerate(texts):
        for target_grade in grades:
            example_text_file = pd.read_csv("fkgl-texts/{grade}.csv".format(grade = target_grade))
            example_text = example_text_file.head(1)
            example = example_text.iloc[0, 0]


            prompts = [
                    'Adjust the following passage for Grade {x} readers. Output only the rewritten text. Do not include any introduction, explanation, or other text.: '.format(x = target_grade), 
                    'Adjust the following passage for Grade {x}  readers in the Flesch-Kincaid Grade scale. Output only the rewritten text. Do not include any introduction, explanation, or other text.: '.format(x = target_grade), 
                    'Adjust the following passage for Grade {x}  readers in the Flesch-Kincaid Grade scale. The Flesch-Kincaid Grade scale looks at total words,  total sentences, and total syllables in a text. Output only the rewritten text. Do not include any introduction, explanation, or other text.: '.format(x = target_grade),
                    'Provide a prompt to adjust the following passage for  Grade {x} readers. Output only the prompt. Do not include any introduction, explanation, or other text. The prompt should specify that only the rewritten text should be output. Do not include any introduction, explanation, or other text. This is the passage: '.format(x = target_grade),
                    'You are a helpful teacher helping a class at Flesch-Kincaid Grade scale {x}. Adjust the following passage to Flesch-Kincaid Grade scale {x} to help your class. Output only the rewritten text. Do not include any introduction, explanation, or other text.: '.format(x = target_grade),
                    'Adjust the following passage for Grade {x}  readers in the Flesch-Kincaid Grade scale. Here is an example of text at this level: '.format(x = target_grade) + example + " Output only the rewritten text. Do not include any introduction, explanation, or other text. This is the passage to adjust: ",
                    'Adjust the following passage for Grade {x}  readers in the Flesch-Kincaid Grade scale. This is the formula for Flesch-Kincaid: Reading grade level = 0.39 (words/sentence) + 11.8 (syllables/word) -15.59. Use this to guide your adjustment. Output only the rewritten text. Do not include any introduction, explanation, or other text. This is the passage: '.format(x = target_grade)
                ]

            for prompt_index, prompt in enumerate(prompts):

                if prompt_index == 4: #this is the meta-prompt
                    response: ChatResponse = chat(model=model, messages=[
                        {
                            'role': 'user',
                            'content': prompt + text,
                        },
                    ])
                        
                    new_prompt = response.message.content
                        
                    response: ChatResponse = chat(model=model, messages=[
                            {
                                'role': 'user',
                                'content': new_prompt,
                            },
                        ])


                    output = response.message.content

                else:
                    
                    response: ChatResponse = chat(model=model, messages=[
                            {
                                'role': 'user',
                                'content': prompt + text,
                            },
                        ])


                    output = response.message.content

                output_fkgl = textstat.flesch_kincaid_grade(output)
                
                # csv format
                # model, grade, text #, prompt #, start text grade, target grade, actual grade

                output_prompt = open("./output/{model}_prompt_output.csv".format(model=model), "a")

                prompt_writer = csv.writer(output_prompt)

                prompt_writer.writerow([output])

                output_csv = open("./output/{model}_out.csv".format(model=model), "a")

                writer = csv.writer(output_csv)

                writer.writerow([model, grade, text_num, prompt_index, f"{texts_fkgl[text_num]:.2f}", target_grade, f"{output_fkgl:.2f}"])




