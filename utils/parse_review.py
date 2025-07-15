

def parse_review(review_loc, hotel_name, page):
    review_id = review_loc.get_attribute('data-review-id')
    # print(review_id)
    review_name_origin = review_loc.locator('div[data-info-type="reviewer-name"]').text_content()
    # print(review_name_origin)
    review_score = review_loc.locator('div.Review-comment-leftScore').text_content()
    # print(review_score)
    review_score_text_loc = review_loc.locator('div.Review-comment-leftScoreText')
    if review_score_text_loc.count() > 0:
        review_score_text = review_score_text_loc.text_content()
    else:
        review_score_text = None
    # print(review_score_text)
    
    trip_type_loc = review_loc.locator('div[data-info-type="group-name"]')
    if trip_type_loc.count() > 0:
        trip_type = trip_type_loc.text_content()
    else:
        trip_type = None
    # print(trip_type)

    room_type_loc = review_loc.locator('div[data-info-type="room-type"]')
    if room_type_loc.count()>0:
        room_type = room_type_loc.text_content()
    else:
        room_type = None
    # print(room_type)

    stay_date_loc = review_loc.locator('div[data-info-type="stay-detail"]')
    if stay_date_loc.count() > 0:
        stay_date = stay_date_loc.text_content()
    else:
        stay_date = None
    # print(stay_date)

    review_title_loc = review_loc.locator('h4[data-testid="review-title"]')
    if review_title_loc.count() > 0 :
        review_title = review_title_loc.text_content()
    else:
        review_title = None
    # print(review_title)

    review_comment_loc = review_loc.locator('p[data-testid="review-comment"]')
    if review_comment_loc.count() > 0 :
        review_comment = review_comment_loc.text_content()
    else:
        review_comment = None
    # print(review_comment)

    review_date_loc = review_loc.locator('div.Review-statusBar-left')
    if review_date_loc.count() > 0:
        review_date = review_date_loc.first.text_content()
    else:
        review_date = page.locator('div.Review-comment-bubble').locator(':scope > div').nth(1).text_content()
    
    # print(review_date)

    dec_review = {
        'hotel_name': hotel_name,
        'review_id':review_id,
        'review_name_origin': review_name_origin,
        'review_score':review_score,
        'review_score_text':review_score_text,
        'trip_type':trip_type,
        'room_type':room_type,
        'stay_date':stay_date,
        'review_title':review_title,
        'review_comment':review_comment,
        'review_date':review_date
    }
    return dec_review