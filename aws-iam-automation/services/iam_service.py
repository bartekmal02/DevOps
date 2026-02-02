import boto3
import json
from botocore.exceptions import ClientError
from exceptions.iam_errors import ResourceCreationError

class IAMManager:
    """Menedżer IAM wykorzystujący profil infra-mgr."""

    def __init__(self, logger):
        # Inicjalizacja sesji z konkretnym profilem administratora
        self.session = boto3.Session(profile_name='infra-mgr')
        self.client = self.session.client('iam')
        self.logger = logger

    def up(self, groups, users):
        """Buduje infrastrukturę IAM."""
        # Konfiguracja grup i uprawnień
        for name, perms in groups.items():
            self._add_group(name)
            self._set_perms(name, perms)

        # Tworzenie userów i przypisanie do grup
        for user, group in users.items():
            self._add_user(user)
            self._join(user, group)

    def down(self, groups, users):
        """Usuwa zasoby (Cleanup)."""
        self.logger.info("Czyszczenie zasobów...")
        for user in users:
            self._rm_user(user)
        for group in groups:
            self._rm_group(group)

    def _add_group(self, name):
        """Tworzy grupę IAM (idempotentnie)."""
        try:
            self.client.create_group(GroupName=name)
            self.logger.info(f"Group {name} OK")
        except self.client.exceptions.EntityAlreadyExistsException:
            pass

    def _set_perms(self, group, actions):
        """Nadaje uprawnienia grupie."""
        policy = {
            "Version": "2012-10-17",
            "Statement": [{"Effect": "Allow", "Action": actions, "Resource": "*"}]
        }
        self.client.put_group_policy(
            GroupName=group,
            PolicyName=f"{group}-Policy",
            PolicyDocument=json.dumps(policy)
        )

    def _add_user(self, name):
        """Tworzy użytkownika."""
        try:
            self.client.create_user(UserName=name)
            self.logger.info(f"User {name} OK")
        except self.client.exceptions.EntityAlreadyExistsException:
            pass

    def _join(self, user, group):
        """Dodaje użytkownika do grupy."""
        try:
            self.client.add_user_to_group(GroupName=group, UserName=user)
        except ClientError as e:
            self.logger.error(f"Join error: {e}")

    def _rm_user(self, name):
        """Usuwa użytkownika z grup i kasuje go."""
        try:
            # Pobranie list grup, do których należy user, aby go wypisać
            res = self.client.list_groups_for_user(UserName=name)
            for g in res.get('Groups', []):
                self.client.remove_user_from_group(GroupName=g['GroupName'], UserName=name)
            self.client.delete_user(UserName=name)
            self.logger.info(f"User {name} removed")
        except ClientError:
            pass

    def _rm_group(self, name):
        """Usuwa politykę i grupę."""
        try:
            self.client.delete_group_policy(GroupName=name, PolicyName=f"{name}-Policy")
            self.client.delete_group(GroupName=name)
            self.logger.info(f"Group {name} removed")
        except ClientError:
            pass