import typer
from hash import hash_data

from db.session import get_db_function
from schemas.role import RoleCreateSchema
from schemas.user import UserCreateSchema
from services.role_service import RoleService
from services.user_service import UserService

app = typer.Typer()


@app.command()
def create_admin_role():
    role_name = "admin"
    role_service = RoleService(get_db_function())
    role_service.create_role(role=RoleCreateSchema(name=role_name))
    return f"Role '{role_name}' successfully created"


@app.command()
def create_superuser(username: str, password: str, email: str):
    user = UserCreateSchema(
        username=username, email=email, password=hash_data(password.encode())
    )
    user_service = UserService(get_db_function())
    role_service = RoleService(get_db_function())

    user_service.create_user(user=user)
    user = user_service.get_user_by_username(username=username)
    role = role_service.get_role_by_name(role_name="admin")

    user_service.assign_role(user, role)
    return "Super user successfully created"


if __name__ == "__main__":
    app()
