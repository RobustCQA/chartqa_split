import pandas as pd
from eval_utils import modified_relaxed_accuracy

chart_type = "complex"
ques_type = "complex"
gen_type = "human"

all_responses = pd.read_json(f"./GPT_final_output/{chart_type}/{ques_type}_{gen_type}.jsonl", lines=True)
responses = all_responses['response']

df = pd.read_json(f"../perturb_jsons/{chart_type}/test_{gen_type}_{ques_type}.json")
questions = df['query'].tolist()
gold_labels = df['label'].tolist()

model_responses = [one_resp['body']['choices'][0]['message']['content'] for one_resp in responses] 

copy = model_responses.copy()
for i, resp in enumerate(copy):
    if(resp[-1] == '.'):
        resp = resp[:-1]
    if 'The answer is: ' in resp:
        x = resp.split('The answer is: ')
        model_responses[i] = x[1]
    elif 'the answer is: ' in resp:
        x = resp.split('the answer is: ')
        model_responses[i] = x[1]
    elif 'The answer is ' in resp:
        x = resp.split('The answer is ')
        model_responses[i] = x[1]
    else:
        print("!!!")

results = list(zip(questions, model_responses))
final_responses = []
for result in results:
    question, response = result
    final_responses.append(response.strip())
    
final_responses = [response.split('=')[-1] for response in final_responses]
final_responses = [response.split('%')[0] for response in final_responses]

model_performance = []
results = list(zip(questions, model_responses))
for i, ans in enumerate(final_responses):
    model_score = modified_relaxed_accuracy(questions[i],gold_labels[i], ans)
    model_performance.append(model_score)

print('Model Performance:', sum(model_performance))
print('Total Questions:', len(model_performance))
print("-------------------")