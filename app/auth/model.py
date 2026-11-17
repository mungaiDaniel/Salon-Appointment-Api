from sqlalchemy import Column, Enum, Integer, String
from werkzeug.security import check_password_hash, generate_password_hash

from app.database.database import db
from app.database.mixins import AuditMixin

ROLES = ("user", "admin", "super_admin")
# Higher number == more privileged.
ROLE_LEVEL = {role: level for level, role in enumerate(ROLES)}

_LEGACY_PREFIX = "$1$"  # md5-crypt hashes written by the original implementation


class User(AuditMixin, db.Model):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    firstName = Column(String(100), nullable=False)
    lastName = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(1000), nullable=False)
    phoneNumber = Column(String(20))
    location = Column(String(100))
    user_role = Column(Enum(*ROLES, name="user_roles"), nullable=False, default="user")

    @staticmethod
    def generate_password_hash(password: str) -> str:
        """Hash a password with Werkzeug's default (scrypt)."""
        return generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        """Check ``password``; transparently upgrade legacy md5-crypt hashes on success."""
        if self.password.startswith(_LEGACY_PREFIX):
            from passlib.hash import md5_crypt

            if not md5_crypt.verify(password, self.password):
                return False
            self.password = self.generate_password_hash(password)
            db.session.commit()
            return True
        return check_password_hash(self.password, password)

    @property
    def role_level(self) -> int:
        return ROLE_LEVEL.get(self.user_role, 0)
