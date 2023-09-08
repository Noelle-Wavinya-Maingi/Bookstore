from database.db import Session
import click
from models import User, BorrowedBook, Fines
from commands.book import TextStyle


@click.group()
def user_commands():
    pass


# Set to store unique usernames
unique_usernames = set()


# Define the 'add-user' command
@user_commands.command()
@click.option("--username", prompt="Add a username", help="Enter the username")
def add_user(username):
    """
    Add a user to the system
    """
    db = Session()
    existing_user = db.query(User).filter(User.username == username).first()

    if existing_user:
        db.close()
        click.echo(f"{TextStyle.RED} {username} already exists.")
        return

    user = User(username=username)
    db.add(user)
    db.commit()
    db.close()
    unique_usernames.add(username)
    click.echo(f"{TextStyle.GREEN} {username} added successfully.")


# Add a new command to list all users and their fine information
@user_commands.command()
def list_users():
    """List all users and their fine information"""

    db = Session()

    # Query the User and Fines tables to get user details and fines
    users_with_fines = (
        db.query(User, Fines).outerjoin(Fines, User.id == Fines.user_id).all()
    )

    # Check if there are no users in the system
    if not users_with_fines:
        # If there are no users, display a message indicating that no users were found
        db.close()
        click.echo(f"{TextStyle.YELLOW}No users found." + TextStyle.RESET)
        return

    # If there are users, display a header indicating "Users:"
    click.echo(f"{TextStyle.CYAN}Users:")

    # Iterate over each user and display their details, including fines
    for user, fine in users_with_fines:
        # Determine if the user has fines and get the fine amount
        if fine is None:
            fine_amount = 0
        else:
            fine_amount = fine.amount

        click.echo(
            f"{TextStyle.BOLD} {TextStyle.CYAN}- Username: {user.username} | Fine Amount: Ksh.{fine_amount} | Arrears: {fine.arrears}"
            + TextStyle.RESET
        )

    db.close()


# Define the 'delete-user' command
@user_commands.command()
@click.option(
    "--username",
    prompt="Enter the username to delete",
    help="Enter the username to delete",
)
def delete_user(username):
    """Delete a user from the system"""

    db = Session()

    user = db.query(User).filter(User.username == username).first()

    if user is None:
        db.close()
        click.echo(f"{TextStyle.RED}User '{username}' not found." + TextStyle.RESET)
        return

    # Check if the user has any borrowed books
    borrowed_book = (
        db.query(BorrowedBook).filter(BorrowedBook.user_id == user.id).first()
    )

    if borrowed_book:
        db.close()
        click.echo(
            f"{TextStyle.RED}Cannot delete user '{username}' as they have borrowed books."
            + TextStyle.RESET
        )
        return

    # Remove the username from the set if it exists
    if username in unique_usernames:
        unique_usernames.remove(username)

    # Delete the user from the database
    db.delete(user)
    db.commit()
    db.close()

    click.echo(
        f"{TextStyle.GREEN}User '{username}' has been deleted from the system."
        + TextStyle.RESET
    )


# Define the 'update-username' command
@user_commands.command()
@click.option(
    "--old-username",
    prompt="Enter the current username",
    help="Enter the current username",
)
@click.option(
    "--new-username", prompt="Enter the new username", help="Enter the new username"
)
def update_username(old_username, new_username):
    """Update a user's username in the system"""

    db = Session()

    # Find the user based on the provided old username
    user = db.query(User).filter(User.username == old_username).first()

    if user is None:
        db.close()
        click.echo(f"{TextStyle.RED} {old_username} not found." + TextStyle.RESET)
        return

    # Check if the new username already exists in the system
    existing_user = db.query(User).filter(User.username == new_username).first()

    if existing_user:
        db.close()
        click.echo(f"{TextStyle.RED} {new_username} already exsists." + TextStyle.RESET)

    # Update the user's username
    user.username = new_username

    # Commit the changes and close the db
    db.commit()
    db.close()

    click.echo(
        f"{TextStyle.GREEN}Username for '{old_username}' has been updated to '{new_username}'."
        + TextStyle.RESET
    )
