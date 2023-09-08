# Bookstore

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![SQLAlchemy Version](https://img.shields.io/badge/sqlalchemy-1.4.46-blue.svg)](https://www.sqlalchemy.org/)
[![Alembic Version](https://img.shields.io/badge/alembic-1.8.1-blue.svg)](https://alembic.sqlalchemy.org/)
[![Click Version](https://img.shields.io/badge/click-8.1.3-blue.svg)](https://click.palletsprojects.com/en/8.1.x/)

A simple command-line bookstore management system built with Python, SQLAlchemy, Alembic, and Click.


## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Commands](#commands)
- [Database Setup](#database-setup)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The Bookstore project is a command-line application for managing a bookstore. It allows users to perform various actions, such as adding users, adding books, borrowing books, returning books, buying books, and more. The project is designed to be a simple yet functional bookstore management system.

## Features

- **User Management:** Add users to the system, list all users, and delete users. Users can also pay fines for late returns.
- **Book Management:** Add books to the system, list all books, delete books, and update book records.
- **Borrowing and Returning:** Borrow books, return books, and keep track of borrowed books and return dates.
- **Sales Records:** Keep track of book sales, including purchase quantity, total amount, and purchase time.
- **Fines Management:** Manage fines for late returns and mark them as paid.
- **Search:** Search for users or books using keywords.
- **Interactive Menu:** Use an interactive menu to choose and execute various options.

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/Noelle-Wavinya-Maingi/Bookstore.git
   ```

2. Navigate to the project directory:

```sh
   cd Phase-3-Project
   ```

3. Install the required Python packages:

```sh
   pip install -r requirements.txt
   ```

4. Set up the database using Alembic:

```sh
   alembic upgrade head
   ```

## Usage

To use the Bookstore management system, follow these steps:

1. Ensure you have Python 3.10+ installed on your system.

2. Install the required packages as described in the installation section.

3. Set up the database using Alembic.

4. Run:

```sh
   python3 main.py
   ```

5. You will be presented with an interactive menu. Choose an option by entering the corresponding number.

6. Follow the prompts to perform various actions suchas adding users, addng books, borrowing books and more.

## Commands

The following commands are available within the interactive menu:

1: Add a user to the system.
2: Add a book to the system.
3: Borrow a book.
4: Return a book.
5: Buy a book.
6: List all books.
7: List all users.
8: List borrowed books.
9: Search for users or books.
10: Update book records.
11: Delete user records.
12: Delete book records.
13: Pay fines for a user.
14: Quit the application.
