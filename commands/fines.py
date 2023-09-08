from database.db import Session
import click
from models import User, Fines
from commands.book import TextStyle


@click.group()
def fines_commands():
    pass


# Define the 'pay-fine' command
@fines_commands.command()
@click.option("--username", prompt="Enter the username", help="Enter the username")
def pay_fine(username):
    """Pay fines for a user"""

    db = Session()

    # Find the user based on the provided username
    user = db.query(User).filter(User.username == username).first()

    if user is None:
        db.close()
        click.echo(f"{TextStyle.RED}User '{username}' not found." + TextStyle.RESET)
        return

    # Check if the user has any unpaid fines
    unpaid_fines = (
        db.query(Fines).filter(Fines.user_id == user.id, Fines.arrears == False).all()
    )

    if not unpaid_fines:
        db.close()
        click.echo(
            f"{TextStyle.YELLOW} {username} has no unpaid fines." + TextStyle.RESET
        )
        return

    # Calculate the total amount of unpaid fines for the user
    total_unpaid_fine_amount = sum(fine.amount for fine in unpaid_fines)

    # Display the total unpaid fine amount and ask for confirmation to pay
    click.echo(
        f"{TextStyle.CYAN}Total unpaid fine amount for '{username}': Ksh.{total_unpaid_fine_amount}"
        + TextStyle.RESET
    )
    confirmation = click.prompt("Do you want to pay the fines? (yes/no)")

    if confirmation.lower() != "yes":
        db.close()
        click.echo(f"{TextStyle.YELLOW}Payment cancelled." + TextStyle.RESET)
        return

    # Mark all unpaid fines for the user as paid
    for fine in unpaid_fines:
        fine.arrears = True

    db.commit()
    db.close()

    click.echo(
        f"{TextStyle.GREEN}Unpaid fines for '{username}' have been paid."
        + TextStyle.RESET
    )
