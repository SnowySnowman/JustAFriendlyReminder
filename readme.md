# Test Cases General Information
- There are four users: Jackie, Marco, Star and Tom.
- Each of them have their own folder with unique name
  which contains the tasks.md and meetings.md each.
- Testing files are located inside folders named as following which can be found under /home/tests:
    - test1
    - test2
    - test3
    
- Please make sure to change each user's tasks.md and
  meetings.md files before running each test case by
  copying respective content from the directory:
  /home/tests/original_files
- Please set your system date as 05/09/23 where it is DD/MM/YY
- Below is instruction on how to change user for each test case.

# Changing User And Running tests
- First, please ensure that the testing users' tasks and meetings
  files are the same as the ones in /home/tests/original_files.
- cd /home/tests
- bash as_{username}.sh < /home/tests/{path_to_testing_file}.in > /home/tests/actual
- diff /home/tests/actual /home/tests/{path_to_testing_file}.out
- when there is nothing being printed out after the last line of code
  input to the terminal, it means that the test was successful.

# Displaying Reminders _ test1
## displaying_reminders_1.in
- Please test as Jackie.
- This test case tests for normal reminder display.
## displaying_reminders_2.in
- Please test as Tom.
- Tests for program skipping invalid date entry.
## displaying_reminders_3.in
- Please test as Star.
- Tests for invalid number input.

# Completing Tasks _ test2
## completing_tasks_1.in
- Please test as Jackie.
- Tests for skipping invalid date task number out of range.
## completing_tasks_2.in
- Please test as Marco.
- Tests for "no task to complete" case.
## completing_tasks_3.in
- Please test as Star.
- Tests for completing tasks valid way.

# Adding New Meetings _ test3
## adding_new_meetings_1.in
- Please test as Marco.
- Tests for adding a new valid meeting and sharing.
## adding_new_meetings_2.in
- Please test as Tom.
- Tests for invalid date, time and inexisting user ID.
## adding_new_meetings_3.in
- Please test as Jackie.
- Tests adding a new valid meeting but not sharing the meeting.
