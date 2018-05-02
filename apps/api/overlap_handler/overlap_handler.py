from django.db import connection

from api.models import ProductionData


def find_time_period_per_segment(prod_data):
    """
    Finds the segment id and latest time connected to it
    :param prod_data: Mapped production data
    :type prod_data: list
    :return: dict of segments and the latest time they were handled
    :rtype: dict
    """
    segment_times = {}
    for data in prod_data:
        if str(data["segment"]) not in segment_times:
            segment_times[str(data["segment"])] = {"earliest_time": data["time"], "latest_time": data["time"]}
        elif data["time"] > segment_times[str(data["segment"])]["latest_time"]:
            segment_times[str(data["segment"])]["latest_time"] = data["time"]
        elif data["time"] < segment_times[str(data["segment"])]["earliest_time"]:
            segment_times[str(data["segment"])]["earliest_time"] = data["time"]

    return segment_times


def delete_prod_data_before_time(segment, time):
    """
    Deletes prod-data older than 'time'
    :param segment: The segment the prod-data belongs to
    :param time: datetime object to use for comparison
    :return: None
    """
    with connection.cursor() as cursor:
        stmt = """
        DELETE FROM api_productiondata
        WHERE segment_id = %s and time < %s
        """
        cursor.execute(stmt, [segment, time])


def remove_outdated_prod_data(segment_times, prod_data):
    """
    Filter out the production data that is already overwritten by production data in db
    :param segment_times: Dict of segments and their corresponding earliest and latest times
    :type segment_times: dict
    :param prod_data: List of mapped production data
    :type prod_data: list
    :return: List of production data that is not outdated
    :rtype: list
    """
    filtered_prod_data = []
    for segment in segment_times:
        # Check if there is not production data on the segment with a more recent time
        if len(ProductionData.objects.filter(segment=segment, time__gt=segment_times[segment]["latest_time"])) == 0:
            for prod in prod_data:
                if str(prod["segment"]) == segment:
                    filtered_prod_data.append(prod)

    return filtered_prod_data


def handle_prod_data_overlap(prod_data):
    """
    Deletes obsolete production data before inserting new
    :param prod_data: Production data mapped to a segment
    :type prod_data: list
    :return: Production data without outdated entries
    :rtype: list
    """
    segment_times = find_time_period_per_segment(prod_data)

    prod_data = remove_outdated_prod_data(segment_times, prod_data)

    # Delete overlap from db
    for segment in segment_times:
        delete_prod_data_before_time(segment, segment_times[segment]["earliest_time"])

    return prod_data
