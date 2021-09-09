from bson import ObjectId

from service.document import DocumentService
from entity.user import User
from util import diff_match_patch as dmp_module

user = User(id=1, name='karthik')

document_service = DocumentService()

dmp = dmp_module.diff_match_patch()

orig_text = 'This is original text'
orig_text = ''
updated_text = 'This is updated text'
more_updated_text = 'This is more updated text !'

diff = dmp.diff_main(text1=orig_text, text2=more_updated_text)
patch = dmp.patch_make(orig_text, more_updated_text)

patch_text = dmp.patch_toText(patch)
patch = dmp.patch_fromText(patch_text)

dmp.patch_apply(patch, orig_text)[0]

document_service.create_document(current_user=user)
document_service.save_diff(current_user=user, document_id='613a0284a50f9184f39bb8c8', changes=patch_text, is_patch=True)

updated_text = document_service.apply_diff(current_user=user, document_id='613a0284a50f9184f39bb8c8')

collection = document_service.mongo_connection.get_collection('user-documents')
collection.find_one({'_id': ObjectId('6139fba1ba9b3284660b3399')})

ObjectId('6139fba1ba9b3284660b3399').__str__()