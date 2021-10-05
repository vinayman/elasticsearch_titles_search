def get_pagination(page_size, page_number, total_elements):
    return dict(
        has_next=page_number * page_size < total_elements,
        has_prev=page_number > 1,
        next_page=page_number + 1,
        prev_page=page_number - 1,
        page=page_number,
    )
