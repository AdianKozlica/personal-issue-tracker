#!/usr/bin/python3
from pathlib import Path

import os
import argparse
import subprocess

ISSUES_DIR = os.path.join(os.getenv('HOME'), '.issues')
INITIAL_TEXT = 'Title: Title Goes Here\nPriority: LOW\n\nContent goes here'
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
        for _ in range(2):
            lines.append(next(file))

    title, priority = lines

    if not title.startswith('Title:'):
        raise SyntaxError('Title not found!')
    
    if not priority.startswith('Priority:'):
        raise SyntaxError('Priority not found!')
    
    title = title.split('Title:')[1].strip()
    priority = priority.split('Priority:')[1].strip()

    if priority not in PRIORITIES:
        raise SyntaxError('Priority must be in', PRIORITIES)
    
    return title, priority

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
        title, priority = parse_metadata(
            os.path.join(ISSUES_DIR, path)
        )
        
        print('Name:', name)
        print('Issue:', title)
        print('Priority:', ansi(priority))
        print()

def get_args():
    parser = argparse.ArgumentParser(
        prog='Personal CLI issue tracker',
    )

    parser.add_argument('-i', '--issues', action='store_true', default=False, help='Lists all issues')
    parser.add_argument('-n', '--new', action='store_true', default=False, help='Creates a new issue')
    parser.add_argument('-d', '--delete', action='store_true', default=False, help='Deletes a issue')
    parser.add_argument('-e', '--edit', action='store_true', default=False, help='Opens an editor for an issue')
    parser.add_argument('--name')

    return parser.parse_args()

def main():
    check_issues_dir()
    
    args = get_args()

    if args.issues:
        get_issues()

    elif args.new:
        new_issue(args.name)

    elif args.edit:
        edit_issue(args.name)
    
    elif args.delete:
        delete_issue(args.name)

if __name__ == '__main__':
    main()