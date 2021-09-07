from service.document import DocumentService
from entity.user import User

user = User(id=1, name='karthik')

document_service = DocumentService()
document_service.save_diff(current_user=user, document_id=1, changes='testing', is_patch=True)