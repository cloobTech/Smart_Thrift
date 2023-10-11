from models import storage
import models


def get_db():
    """Get DB Instance"""
    try:
        yield storage
    except Exception:
        storage.rollback()
    finally:
        storage.shutdown_db()


def hyper_media_pagination(cls, page=1, page_size=7, column: str | None = None, search: str | None = None):
    """Formatted Pagination"""
    dict_obj, total_pages, total_items = storage.paginate(
        cls, page, page_size, search_column=column, search_query=search)
    prev = page - 1 if page > 1 else None
    next = page + 1 if page < total_pages else None

    data = []
    if cls == models.user_profile.UserProfile:
        for key in dict_obj.keys():
            obj = dict_obj[key]
            obj_dict = obj.to_dict()
            obj_dict['email'] = obj.user.email
            data.append(obj_dict)


    return {
        # "data": [dict_obj[key].to_dict() for key in dict_obj.keys()],
        "data": data,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "total_items": total_items,
        "prev": prev,
        "next": next,
    }
