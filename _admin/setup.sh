#!/bin/bash

# Log file path
LOG_FILE="$(dirname "$0")/setup_log_$(date +"%Y%m%d").txt"

# Function to log messages
log_message() {
    echo "$1"
    echo "$1" >> "$LOG_FILE"
}

# Function to handle errors
handle_error() {
    log_message "Error: $1"
    rm symbolic_link_error.txt  # Remove the temporary file
}

# Function to check if command is available
check_command() {
    if ! command -v "$1" &> /dev/null; then
        handle_error "$2"
    fi
}

# Function to run a MySQL command
run_mysql_command() {
    mysql -h "$MYSQL_HOST" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "$1"
}

# Function to create MySQL database if not exists
create_mysql_database() {
    run_mysql_command "CREATE DATABASE IF NOT EXISTS $MYSQL_DATABASE;"
}

# Log the script start time
log_message "Script started at: $(date)"

# Attempt to create symbolic link
if ln -s /usr/local/mysql/bin/mysql /usr/local/bin/mysql 2> symbolic_link_error.txt; then
    log_message "Successfully created a symbolic link for MySQL executable."
else
    handle_error "Failed to create a symbolic link for MySQL executable. Reason: $(cat symbolic_link_error.txt)"
fi

# Check if 'mysql' command is available
check_command "mysql" "MySQL Server is not installed. Please download and install it from https://dev.mysql.com/downloads/"

# Get MySQL credentials and database name from user
read -p "Enter MySQL host (default: localhost): " MYSQL_HOST
MYSQL_HOST=${MYSQL_HOST:-localhost}
log_message "MySQL host: $MYSQL_HOST"

read -p "Enter MySQL user (default: root): " MYSQL_USER
MYSQL_USER=${MYSQL_USER:-root}
log_message "MySQL user: $MYSQL_USER"

read -s -p "Enter MySQL password: " MYSQL_PASSWORD
echo
log_message "MySQL password: ********"

read -p "Enter MySQL database name (default: trading_joe): " MYSQL_DATABASE
MYSQL_DATABASE=${MYSQL_DATABASE:-trading_joe}
log_message "MySQL database name: $MYSQL_DATABASE"

# Create MySQL database if not exists
create_mysql_database

# Run each Python script based on user input
run_python_script() {
    script_name="$1"
    read -p "Do you want to run $script_name? (Y/N): " run_script

    if [[ "$run_script" == "Y" || "$run_script" == "y" ]]; then
        log_message "Running $script_name..."
        # Additional logic for the specific Python script if needed
        log_message "$script_name executed."
    else
        log_message "$script_name skipped as per user choice."
    fi
}

# Run each Python script based on user input
run_python_script "create_all_tables.py"
run_python_script "sync_instruments.py"
run_python_script "sync_listings.py"

# Log the script completion time
log_message "Script completed at: $(date)"
