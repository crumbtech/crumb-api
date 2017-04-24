from src.models import Crumb
from src.database import db_session


def test_create_crumb(crumb_dict):
    """ successfully creates a crumb record
    """
    crumb = Crumb(**crumb_dict)
    with db_session() as session:
        session.add(crumb)
        session.commit()
        persisted_crumb = session.query(Crumb).first()
        assert isinstance(persisted_crumb.id, int) is True
        session.delete(persisted_crumb)
