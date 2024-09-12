#!/usr/bin/python3
from datetime import datetime
from pathlib import Path

import os
import json
import argparse
import subprocess

def get_current_datetime():
    return datetime.now().strftime('%d-%m-%Y %H:%M')

def validate_grid(n: str):
    n = int(n)
    
    if n < 1:
        raise RuntimeError('Grid number must be greater or equal to 1')

    return n

ISSUES_DIR = os.path.join(os.getenv('HOME'), '.issues')
PRIORITIES = { 'LOW', 'MEDIUM', 'HIGH' }

def check_issues_dir(issues_dir: str):
    if not os.path.exists(issues_dir):
        os.mkdir(issues_dir)

def chunks(l: list, n: int):
    return [l[i:i + n] for i in range(0, len(l), n)]

def get_initial_text(name: str):
    return f'Title: {name}\nPriority: LOW\nDue: {get_current_datetime()}\n\nContent goes here'

def ansi(priority: str):
    match priority:
        case 'LOW':
            return '\x1b[38;2;255;255;255m▄\x1b[0m\x1b[38;2;128;128;128m▆█\x1b[0m'
        case 'MEDIUM':
            return '\x1b[38;2;255;255;255m▄▆\x1b[0m\x1b[38;2;128;128;128m█\x1b[0m'
        case _:
            return '\x1b[38;2;255;255;255m▄▆█\x1b[0m'

def get_priority_num(priority: str):
    match priority:
        case 'HIGH':
            return 2
        case 'MEDIUM':
            return 1
        case _:
            return 0

def get_issue_path(issues_dir: str, name: str, check_if_exists=False):
    issue_path = os.path.join(issues_dir, f'{name}.md')

    if check_if_exists:
        if not os.path.exists(issue_path):
            raise FileNotFoundError()

    return issue_path

def open_with_editor(path: str):
    subprocess.call(['/usr/bin/editor', path])

def parse_metadata(path: str):
    lines: list[str] = []
    
    with open(path, 'r') as file:
        for _ in range(3):
            lines.append(next(file))

    title, priority, due = lines

    if not title.startswith('Title:'):
        raise SyntaxError('Title not found!')
    
    if not priority.startswith('Priority:'):
        raise SyntaxError('Priority not found!')
    
    priority = priority.split('Priority:')[1].strip().upper()

    if priority not in PRIORITIES:
        raise SyntaxError('Priority must be in', PRIORITIES)
    
    return title.strip(), priority, due.strip()

def new_issue(issues_dir: str, name: str):
    if not name:
        raise RuntimeError('Name must not be empty')

    issue_path = get_issue_path(issues_dir, name)

    if os.path.exists(issue_path):
        raise FileExistsError()
    
    with open(issue_path, 'w') as file:
        file.write(
            get_initial_text(name)
        )
    
    open_with_editor(issue_path)

def edit_issue(issues_dir: str, name: str):
    if not name:
        raise RuntimeError('Name must not be empty')

    issue_path = get_issue_path(issues_dir, name, True)
    open_with_editor(issue_path)

def delete_issue(issues_dir: str, name: str):
    if not name:
        raise RuntimeError('Name must not be empty')
    
    issue_path = get_issue_path(issues_dir, name, True)
    os.remove(issue_path)

def get_issue_list(
    issues_dir: str,
    sort: str,
    wanted_priority: str | None = None 
):
    issue_list = []

    for path in os.listdir(issues_dir):
        name = Path(path).stem
        title, priority, due = parse_metadata(
            os.path.join(issues_dir, path)
        )
        if wanted_priority:
            if priority != wanted_priority:
                continue
        
        issue_list.append([name, title, priority, due])
    
    issue_list.sort(
        key=lambda item: get_priority_num(item[2]), 
        reverse=False if sort == 'asc' else True
    )

    return issue_list

def get_issues_json(
    issues_dir: str,
    sort: str,
    wanted_priorty: str | None = None
):
    issue_list = get_issue_list(
        issues_dir,
        sort,
        wanted_priorty,
    )

    issues_json_list = []

    for name, title, priority, due in issue_list:
        issues_json_list.append({
            'name': name,
            'title': title.split('Title:')[1].strip(),
            'priority': priority,
            'due': due.split('Due:')[1].strip()
        })
    
    print(
        json.dumps(
            { 'issues': issues_json_list }, 
            indent=2
        )
    )

def get_issues(
    issues_dir: str, 
    sort: str, 
    wanted_priority: str | None = None,
    grid = 2
):
    issue_list =  get_issue_list(
        issues_dir,
        sort,
        wanted_priority
    )

    max_len = 0

    for issue in issue_list:
        for item in issue:
            max_len = max(max_len, len(item))

    for chunk in chunks(issue_list, grid):
        for j in range(4):
            for i in range(len(chunk)):
                string = chunk[i][j]
                str_len = len(string)
                subtract = 0

                if j == 0:
                    string = f'Name: {string}'
                    str_len += len('Name: ')

                elif j == 2:
                    if string == 'HIGH':
                        subtract = 1
                    elif string == 'MEDIUM':
                        subtract = 3

                    string = f'Priority: {ansi(string)}'
                    str_len += len('Priority: ')
                    
                print('|' if i == 0 else '', string, end=' ' * (abs(str_len - max_len - subtract) + 2) + '|') # This works......
            print()
        print()

def get_args():
    parser = argparse.ArgumentParser(
        prog='Personal CLI issue tracker',
    )

    parser.add_argument('-n', '--new', help='Create a new issue.')
    parser.add_argument('-d', '--delete', help='Delete an issue by name.')
    parser.add_argument('-e', '--edit', help='Edit an existing issue by name.')
    
    parser.add_argument(
        '-s', 
        '--sort', 
        choices=['asc', 'desc'], 
        default='desc', 
        help='Sort issues by priority.',
        type=str.lower
    )
    
    parser.add_argument(
        '-p', '--priority', 
        choices=['LOW', 'MEDIUM', 'HIGH'],
        type=str.upper,
        help='Filter issues by priority level.'
    )

    parser.add_argument(
        '--directory',
        default=ISSUES_DIR,
        help='Specify a custom directory for storing issues.',
        type=os.path.expanduser
    )

    parser.add_argument(
        '--grid',
        default=2,
        help='Display issues in an N x N grid format.',
        type=validate_grid
    )

    parser.add_argument(
        '--json',
        action='store_true',
        default=False,
        help='JSON Output',
    )

    return parser.parse_args()

def main():
    args = get_args()
    
    check_issues_dir(args.directory)

    if args.new:
        new_issue(args.directory, args.new)

    elif args.edit:
        edit_issue(args.directory, args.edit)
    
    elif args.delete:
        delete_issue(args.directory, args.delete)

    elif args.json:
        get_issues_json(args.directory, args.sort, args.priority)

    else:
        get_issues(args.directory, args.sort, args.priority, args.grid)

if __name__ == '__main__':
    main()