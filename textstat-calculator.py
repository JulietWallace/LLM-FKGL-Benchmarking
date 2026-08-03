from ollama import chat
from ollama import ChatResponse
import textstat
from textstat import flesch_kincaid_grade
import pandas as pd
import csv
import time

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
                    'Adjust the following passage for Grade {x} readers. Output ONLY the rewritten text without any additional explanation: '.format(x = target_grade), 
                    'Adjust the following passage for Grade {x}  readers on the Flesch-Kincaid Grade scale. Output ONLY the rewritten text without any additional explanation: '.format(x = target_grade), 
                    'Adjust the following passage for Grade {x}  readers on the Flesch-Kincaid Grade scale. The Flesch-Kincaid Grade scale looks at total words,  total sentences, and total syllables in a text. Output ONLY the rewritten text without any additional explanation: '.format(x = target_grade),
                    'Provide a prompt to adjust the following passage for  Grade {x} readers. Output ONLY the prompt without any additional explanation. The prompt should specify that only the rewritten text should be output. Do not include any introduction, explanation, or other text. This is the passage: '.format(x = target_grade),
                    'You are a helpful teacher helping a class at Flesch-Kincaid Grade scale {x}. Adjust the following passage to Flesch-Kincaid Grade scale {x} to help your class. Output ONLY the rewritten text without any additional explanation: '.format(x = target_grade),
                    'Adjust the following passage for Grade {x}  readers in the Flesch-Kincaid Grade scale. Here is an example of text at this level: '.format(x = target_grade) + example + " Output ONLY the rewritten text without any additional explanation This is the passage to adjust: ",
                    'Adjust the following passage for Grade {x}  readers in the Flesch-Kincaid Grade scale. This is the formula for Flesch-Kincaid: Reading grade level = 0.39 (words/sentence) + 11.8 (syllables/word) -15.59. Use this to guide your adjustment. Output ONLY the rewritten text without any additional explanation. This is the passage: '.format(x = target_grade)
                ]

            for prompt_index, prompt in enumerate(prompts):

                if prompt_index == 4: #this is the meta-prompt
                    start = time.perf_counter()
                    response: ChatResponse = chat(model=model, messages=[
                        {
                            'role': 'user',
                            'content': prompt + text,
                        },
                    ])
                        
                    new_prompt = response.message.content

                    end_prompt_time = time.perf_counter()

                    second_start = time.perf_counter()
                        
                    response: ChatResponse = chat(model=model, messages=[
                            {
                                'role': 'user',
                                'content': new_prompt,
                            },
                        ])

                    output = response.message.content
                    end = time.perf_counter()

                    prompt_time = end_prompt_time - start

                    output_time = end - second_start



                    meta_prompts = open("output/timed/meta_prompts/{model}_meta_prompts.csv".format(model=model), "a")
                    prompts_writer = csv.writer(meta_prompts)
                    prompt_writer.writerow([grade, text_num, target_grade, new_prompt, f"{prompt_time:.3f}"])

                else:

                    start = time.perf_counter() 
                    response: ChatResponse = chat(model=model, messages=[
                            {
                                'role': 'user',
                                'content': prompt + text,
                            },
                        ])


                    output = response.message.content
                    end = time.perf_counter()

                    output_time = end - start

                output_fkgl = textstat.flesch_kincaid_grade(output)
                
                # csv format
                # model, grade, text #, prompt #, start text grade, target grade, actual grade

                output_prompt = open("./output/timed/{model}_prompt_output.csv".format(model=model), "a")

                prompt_writer = csv.writer(output_prompt)

                prompt_writer.writerow([model, grade, text_num, target_grade, prompt_index, output])

                output_csv = open("./output/timed/{model}_out.csv".format(model=model), "a")

                writer = csv.writer(output_csv)

                writer.writerow([model, grade, text_num, prompt_index, f"{texts_fkgl[text_num]:.2f}", target_grade, f"{output_fkgl:.2f}", f"{output_time:.3f}"])




