from application.settings import START_PAGIN, LIMIT_PAGIN


def paginate_results(req_parser, base_url, f, *paras):
    pagin_paras = req_parser.parse_args()
    start = pagin_paras['start']
    limit = pagin_paras['limit']
    result = {"previous": None, "next": None, "data": None}
    if (start is not None and start >= 0) and (limit is not None and limit >0):
        pre_start = max(0, start - limit)
        result['previous'] = base_url + "?start=" + str(pre_start) + "&limit=" + str(start)
    else:
        start = START_PAGIN
        limit = LIMIT_PAGIN
    data = f(start, limit, *paras)
    result['data'] = data
    if len(result['data']) == limit:
        result['next'] = base_url + "?start=" + str(start + limit) + "&limit=" + str(limit)
    return result