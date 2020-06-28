import gap_scorer 
import csv



with open('gap-test.tsv', 'r') as f:
    reader = csv.DictReader(f, fieldnames=gap_scorer.GOLD_FIELDNAMES, delimiter='\t')
    rows = list(reader)[1:]


list_answer = list()
for i, row in enumerate(rows):
    p_idx = int(row['Pronoun-offset'])
    b_idx = int(row['B-offset'])
    a_idx = int(row['A-offset'])

    # check whether the pronoun is placed before the A or B. 
    distance_a = p_idx - a_idx
    distance_b = p_idx - b_idx

    # A should not be a named entitiy if it behinds the pronoun
    if a_idx > p_idx:
        answer_a = "FALSE"
        answer_b = "TRUE"

    # B should not be a named entitiy if it behinds the pronoun
    elif b_idx > p_idx:
       answer_a = "TRUE"
       answer_b = "FALSE"

    # Further one should be the named entitiy
    elif distance_a > distance_b:
        answer_a = "FALSE"
        answer_b = "TRUE"
    else:
        answer_a = "TRUE"
        answer_b = "FALSE"

    # Append to the result
    list_answer.append((i, answer_b, answer_a))



def write_prediction(list_answer):
    with open('snippet_output_20170634.tsv', 'w') as output:
        for idx, a, b in list_answer:
            # a = 'TRUE' if a else 'FALSE'
            # b = 'TRUE' if b else 'FALSE'
            row = f'test-{idx+1}\t{a}\t{b}\n'
            output.write(row)
    with open('page_output_20170634.tsv', 'w') as output:
        for idx, a, b in list_answer:
            # a = 'TRUE' if a else 'FALSE'
            # b = 'TRUE' if b else 'FALSE'
            row = f'test-{idx+1}\t{a}\t{b}\n'
            output.write(row)

write_prediction(list_answer)

snippet_result = gap_scorer.run_scorer('gap-test.tsv','snippet_output_20170634.tsv')
print(snippet_result)
print("===============================")

page_result = gap_scorer.run_scorer('gap-test.tsv','page_output_20170634.tsv')
print(page_result)