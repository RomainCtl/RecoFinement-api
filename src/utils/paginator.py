from sqlalchemy import func
import math

from settings import PAGE_SIZE


class Paginator:
    @staticmethod
    def get_from(query, page_number=1):
        page_size = PAGE_SIZE
        offset = (page_number - 1) * page_size

        total_elem = query.count()
        if offset < 0:
            return [], math.ceil(total_elem / page_size)

        datas = query.offset(offset).limit(page_size).all()

        return datas, math.ceil(total_elem / page_size)
