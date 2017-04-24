from src.models import CrumbImage
from src.models import Crumb
from src.database import db_session


def test_create_crumb_image(crumb_image_dict):
    """ successfully creates a crumb image record
    """
    crumb_image = CrumbImage(**crumb_image_dict)
    with db_session() as session:
        session.add(crumb_image)
        session.commit()
        persisted_crumb_image = session.query(CrumbImage).first()
        assert isinstance(persisted_crumb_image.id, int) is True
        assert persisted_crumb_image.user.id == crumb_image_dict['user_id']
        assert persisted_crumb_image.crumb.id == crumb_image_dict['crumb_id']
        crumb = session.query(Crumb).get(crumb_image_dict['crumb_id'])
        assert len(crumb.crumb_images) == 1
        session.delete(persisted_crumb_image)
