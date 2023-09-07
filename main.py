from database.db import Base, engine
import click

#Define a CLI group
@click.group()
def cli():
    pass

#Helper function to print a separator
def print_separator():
    print("\n" + "*" * 70 + "\n")

#Define the main menu command
@cli.command()
def menu():
    """Main Menu - Choose an option"""

    print_separator()

    click.echo("Choose an option:")
    click.echo("1. Add a user")
    click.echo("2. Add a book")
    click.echo("3. Borrow a book")
    click.echo("4. Return a book")
    click.echo("5. List of books")
    click.echo("6. Buy a book")
    click.echo("7. Quit")

    print_separator()

    option = click.prompt("Enter an option number")
    while True:
        execute_option(option)
        if option == "7":
            break

#Helper function to execute chosen options
def execute_option(option):
    while option not in ["1", "2", "3", "4", "5", "6", "7"]:
        click.echo("Invalid option. Please choose a valid option.")
        option = click.prompt("Enter a valid option")


cli.add_command(menu)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    while True:
        menu()
