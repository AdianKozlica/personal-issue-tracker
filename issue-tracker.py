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

def check_issues_dir(issues_dir: str):
    if not os.path.exists(issues_dir):
        os.mkdir(issues_dir)

def get_color(priority: str):
    match priority:
        case 'LOW':
            return '\x1b[38;2;0;0;255m'
        case 'MEDIUM':
            return '\x1b[38;2;255;255;0m'
        case 'HIGH':
            return '\x1b[38;2;255;0;0m'
    
    return '\x1b[38;2;255;0;0'

def ansi(priority: str):
    COLOR = get_color(priority)
    return f'{COLOR}{priority}\033[0m'

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
        file.write(INITIAL_TEXT)
    
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

def get_issues(issues_dir: str, sort: str, wanted_priority: str | None = None):
    issue_list: list[list[str]] = []

    for path in os.listdir(issues_dir):
        name = Path(path).stem
        title, priority, due = parse_metadata(
            os.path.join(issues_dir, path)
        )
        
        issue_list.append([name, title, priority, due])
    
    issue_list.sort(
        key=lambda item: get_priority_num(item[2]), 
        reverse=False if sort == 'asc' else True
    )

    for name, title, priority, due in issue_list:
        if wanted_priority:
            if priority != wanted_priority:
                continue 

        print('Name:', name)
        print(title)
        print('Priority:', ansi(priority))
        print(due)
        print()

def get_args():
    parser = argparse.ArgumentParser(
        prog='Personal CLI issue tracker',
    )

    parser.add_argument('-n', '--new', help='Creates a new issue')
    parser.add_argument('-d', '--delete', help='Deletes a issue')
    parser.add_argument('-e', '--edit', help='Opens an editor for an issue')
    parser.add_argument(
        '-s', 
        '--sort', 
        choices=['asc', 'desc'], 
        default='desc', 
        help='Sort by issue priority',
        type=str.lower
    )
    parser.add_argument(
        '-p', '--priority', 
        choices=['LOW', 'MEDIUM', 'HIGH'],
        type=str.upper,
        help='Search by priority'
    )

    parser.add_argument(
        '--directory',
        default=ISSUES_DIR,
        help='Custom issues directory',
        type=os.path.expanduser
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

    else:
        get_issues(args.directory, args.sort, args.priority)

if __name__ == '__main__':
    main()