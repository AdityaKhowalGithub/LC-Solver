import requests
from pygments import highlight
from pygments.lexers import JavaLexer, PythonLexer
from pygments.formatters import TerminalFormatter


def get_solution(prompt, language):
    """
    Uses the ChatGPT API to generate a solution for the given prompt in the
    specified language (Python or Java).
    """
    # Set up the API call
    headers = {'Authorization': 'Bearer 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'}
    params = {
        'model': 'text-davinci-002',
        'prompt': prompt,
        'temperature': 0.5,
        'max_tokens': 1024,
        'stop': ['\n\n']
    }
    if language == '1':
        params['temperature'] = 0.7
        params['prompt'] += '\n\ndef solution():\n    '
        params['engine'] = 'davinci-codex'
    elif language == '2':
        params['prompt'] += '\n\npublic static void main(String[] args) {\n    '
        params['engine'] = 'davinci-codex'
    else:
        return 'Invalid input.'

    # Call the API and extract the solution
    response = requests.post('https://api.openai.com/v1/engines/' + params['engine'] + '/completions', headers=headers, json=params)
    if response.status_code != 200:
        return 'Error: ' + response.text
    solution = response.json()['choices'][0]['text']

    # Add comments to the solution to explain the logic
    comments = ''
    if language == '1':
        comments += '# Solution to the given LeetCode problem using Python\n\n'
        comments += '# Define the solution function\n\n'
        comments += '# Your solution logic goes here\n\n'
        comments += 'return # Your solution output goes here'
    elif language == '2':
        comments += '// Solution to the given LeetCode problem using Java\n\n'
        comments += 'public static void solution() {\n'
        comments += '    // Your solution logic goes here\n'
        comments += '}\n\n'
        comments += 'public static void main(String[] args) {\n'
        comments += '    solution();\n'
        comments += '}'

    # Format the solution and comments for display
    if language == '1':
        lexer = PythonLexer()
    elif language == '2':
        lexer = JavaLexer()
    formatter = TerminalFormatter(bg='dark')
    formatted_solution = highlight(solution, lexer, formatter)
    formatted_comments = highlight(comments, lexer, formatter)

    return f'{formatted_solution}\n\n{formatted_comments}'


# Main program loop
while True:
    # Get user input
    print('\nEnter the LeetCode-style coding question (or "quit" to exit):')
    prompt = input().strip()
    if prompt == 'quit':
        break

    print('\nSelect the output language:\n\n  1. Python\n  2. Java\n')
    language = input().strip()
    solution = get_solution(prompt, language)

    print(f'\n{solution}')

    # Refine the solution with test inputs and expected outputs
    while True:
        print('\nDo you want to refine the solution with test cases and expected outputs? (y/n)')
        choice = input().strip().lower()
        if choice == 'y':
            print('\nEnter a test case input:')
            test_input = input().strip()
            print('\nEnter the expected output for the test case:')
            expected_output = input().strip()

            # Set up the API call to refine the solution
            headers = {'Authorization': 'Bearer <INSERT YOUR CHATGPT API TOKEN HERE>'}
            params = {
                'model': 'text-davinci-002',
                'prompt': f'{prompt}\n\nTest case: {test_input}\nExpected output: {expected_output}\n\n',
                'temperature': 0.5,
                'max_tokens': 1024,
                'stop': ['\n\n']
            }
            if language == '1':
                params['temperature'] = 0.7
                params['prompt'] += 'def solution():\n    '
                params['engine'] = 'davinci-codex'
            elif language == '2':
                params['prompt'] += 'public static void solution() {\n    '
                params['engine'] = 'davinci-codex'
            else:
                print('Invalid input.')
                break

            # Call the API and update the solution
            response = requests.post('https://api.openai.com/v1/engines/' + params['engine'] + '/completions', headers=headers, json=params)
            if response.status_code != 200:
                print('Error: ' + response.text)
                break
            solution = response.json()['choices'][0]['text']

            # Format the solution and comments for display
            if language == '1':
                lexer = PythonLexer()
            elif language == '2':
                lexer = JavaLexer()
            formatter = TerminalFormatter(bg='dark')
            formatted_solution = highlight(solution, lexer, formatter)

            print(f'\nRefined solution for input "{test_input}" and expected output "{expected_output}":\n\n{formatted_solution}')
        elif choice == 'n':
            break
        else:
            print('Invalid input.')
            continue
