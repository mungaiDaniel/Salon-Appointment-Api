"""Flask CLI commands (run with ``flask <command>``)."""

import click
from flask import Flask
from sqlalchemy import select

from app.auth.model import ROLES, User
from app.database.database import db


def register_cli(app: Flask) -> None:
    @app.cli.command("create-admin")
    @click.argument("email")
    @click.password_option()
    @click.option("--first-name", default="Admin", show_default=True)
    @click.option("--last-name", default="User", show_default=True)
    @click.option("--role", type=click.Choice(ROLES[1:]), default="super_admin", show_default=True)
    def create_admin(email, password, first_name, last_name, role):
        """Create (or promote) a staff account; the API has no public way to make the first one."""
        if len(password) < 8:
            raise click.ClickException("Password must be at least 8 characters.")
        email = email.strip().lower()
        user = db.session.execute(select(User).filter_by(email=email)).scalar_one_or_none()
        if user:
            user.user_role = role
            click.echo(f"Promoted existing user {email} to {role}.")
        else:
            user = User(
                firstName=first_name,
                lastName=last_name,
                email=email,
                password=User.generate_password_hash(password),
                user_role=role,
                created_by="CLI",
            )
            db.session.add(user)
            click.echo(f"Created {role} {email}.")
        db.session.commit()
