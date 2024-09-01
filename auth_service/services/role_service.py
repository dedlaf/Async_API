from schemas.role import Role


class RoleService:

    def create_role(self, role: str) -> None:
        ...

    def get_role(self, role_id: str) -> Role:
        ...

    def get_roles(self) -> list[Role]:
        ...

    def update_role(self, role_id: str, role: str) -> None:
        ...

    def delete_role(self, role_id: str) -> None:
        ...

