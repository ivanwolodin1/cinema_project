def prepare_bulk_query(index, es_data):
    bulk_query = []
    for row in es_data:
        es_data = {'_index': index, '_id': row['id']}
        es_data.update({'_source': row})
        bulk_query.append(es_data)
    return bulk_query
