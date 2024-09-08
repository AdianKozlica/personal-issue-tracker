#!/usr/bin/python3
from datetime import datetime
from pathlib import Path

import os
import argparse
import subprocess

def get_current_datetime():
    return datetime.now().strftime('%d-%m-%Y %H:%M')

ISSUES_DIR = os.path.join(os.getenv('HOME'), '.issues')
INITIAL_TEXT = f'Title: Title Goes Here\nPriority: LOW\nDue: {get_current_datetime()}\n\nContent goes here'
PRIORITIES = { 'LOW', 'MEDIUM', 'HIGH' }

def check_issues_dir():
    if not os.path.exists(ISSUES_DIR):
        os.mkdir(ISSUES_DIR)

def get_color(priority: str):
    match priority:
        case 'LOW':
            return '\x1b[48;2;0;0;255m'
        case 'MEDIUM':
            return '\x1b[48;2;255;255;0m'
        case 'HIGH':
            return '\x1b[48;2;255;0;0m'
    
    return '\x1b[48;2;255;0;0'

def ansi(priority: str):
    COLOR = get_color(priority)
    return f'{COLOR}{priority}\033[0m'

def get_issue_path(name: str, check_if_exists=False):
    issue_path = os.path.join(ISSUES_DIR, f'{name}.md')

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
    
    priority = priority.split('Priority:')[1].strip()

    if priority not in PRIORITIES:
        raise SyntaxError('Priority must be in', PRIORITIES)
    
    return title.strip(), priority, due.strip()

def new_issue(name: str):
    if not name:
        raise RuntimeError('Name must not be empty')

    issue_path = get_issue_path(name)

    if os.path.exists(issue_path):
        raise FileExistsError()
    
    with open(issue_path, 'w') as file:
        file.write(INITIAL_TEXT)
    
    open_with_editor(issue_path)

def edit_issue(name: str):
    if not name:
        raise RuntimeError('Name must not be empty')

    issue_path = get_issue_path(name, True)
    open_with_editor(issue_path)

def delete_issue(name: str):
    if not name:
        raise RuntimeError('Name must not be empty')
    
    issue_path = get_issue_path(name, True)
    os.remove(issue_path)

def get_issues():
    for path in os.listdir(ISSUES_DIR):
        name = Path(path).stem
        title, priority, due = parse_metadata(
            os.path.join(ISSUES_DIR, path)
        )
        
        print('Name:', name)
        print(title)
        print('Priority:', ansi(priority))
        print(due)

def get_args():
    parser = argparse.ArgumentParser(
        prog='Personal CLI issue tracker',
    )

    parser.add_argument('-i', '--issues', action='store_true', default=False, help='Lists all issues')
    parser.add_argument('-n', '--new', help='Creates a new issue')
    parser.add_argument('-d', '--delete', help='Deletes a issue')
    parser.add_argument('-e', '--edit', help='Opens an editor for an issue')

    return parser.parse_args()

def main():
    check_issues_dir()
    
    args = get_args()

    if args.issues:
        get_issues()

    elif args.new:
        new_issue(args.new)

    elif args.edit:
        edit_issue(args.edit)
    
    elif args.delete:
        delete_issue(args.delete)

if __name__ == '__main__':
    main()