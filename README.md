# Personal CLI Issue Tracker

This is a command-line interface (CLI) tool for tracking issues. It allows you to create, delete, and edit issues directly from the terminal.

## Features

- **Create a new issue**: Add a new issue to the tracker.
- **Delete an issue**: Remove an issue from the tracker by its name.
- **Edit an issue**: Modify an existing issue by its name.
- **Sort issues**: Sort issues by priority.
- **Filter issues**: Filter issues by priority level.
- **Specify custom directory**: Use a custom directory for storing issues.
- **Display issues in grid format**: Display issues in an N x N grid format.
- **Output issues in JSON format**: Output issues in JSON format.
- **Output issues in CSV format**: Output issues in CSV format.

## Usage

### Command Line Arguments

The CLI accepts the following arguments:

- `-n`, `--new`: Create a new issue.
- `-d`, `--delete`: Delete an issue by name.
- `-e`, `--edit`: Edit an existing issue by name.
- `-s`, `--sort`: Sort issues by priority (`asc` or `desc`).
- `-p`, `--priority`: Filter issues by priority level (`LOW`, `MEDIUM`, `HIGH`).
- `--directory`: Specify a custom directory for storing issues.
- `--grid`: Display issues in an N x N grid format.
- `--json`: Output issues in JSON format.
- `--csv`: Output issues in CSV format.

### Example Output

Here is an example of what the output might look like when displaying issues:
```sh
| Name: Issue                    | Name: Issue2                      |
| Title: Some title              | Title: Some title2                |
| Priority: ▄▆█                  | Priority: ▄▆█                     |
| Due: 10-09-2024 00:30          | Due:                              |

| Name: Issue3                   |
| Title: Title3                  |
| Priority: ▄▆█                  |
| Due: NOT RESTRICTED TO FORMAT  |
```
### Example Commands

- **Create a new issue**:
  ```sh
  python issue-tracker.py -n "Issue Name"
  ```

- **Delete an issue**:
  ```sh
  python issue-tracker.py -d "Issue Name"
  ```

- **Edit an issue**:
  ```sh
  python issue-tracker.py -e "Issue Name"
  ```

- **Sort issues by priority:**:
  ```sh
  python issue-tracker.py -s asc
  ```

- **Filter issues by priority:**:
  ```sh
  python issue-tracker.py -p HIGH
  python issue-tracker.py -p HIGH MEDIUM
  ```

- **Specify a custom directory for storing issues:**:
  ```sh
  python issue-tracker.py --directory /path/to/custom/directory
  ```

- **Display issues in a 3x3 grid format:**:
  ```sh
  python issue-tracker.py --grid 3
  ```

- **Output issues in JSON format:**:
  ```sh
  python issue-tracker.py --json
  ```

- **Output issues in CSV format:**:
  ```sh
  python issue-tracker.py --csv
  ```

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/AdianKozlica/personal-issue-tracker.git
   ```
2. Navigate to the project directory:
   ```sh
   cd issue-tracker
   ```
3. Run the script with the desired arguments.

## License

This project is licensed under the GPL 2.0 License. See the [`LICENSE`](LICENSE) file for details.