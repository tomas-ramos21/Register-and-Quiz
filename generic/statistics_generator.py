import csv
from django.http import StreamingHttpResponse

class stat_generator:
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        return value


def attendance_stats_csv(data_dict):
    """A view that streams a large CSV file."""
    # Generate a sequence of rows. The range is based on the maximum number of
    # rows that can be handled by a single sheet in most spreadsheet
    # applications.
    rows = []

    for label, date_attendance_pair in data_dict.items():
        str1 = ''
        str1 = label
        for date, attendance in date_attendance_pair:
            str1 = str1 + str(date) + ',' + str(attendance)
            rows.append(str1)

    pseudo_buffer = stat_generator()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows), content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="attendance_stats.csv"'
    return response
	
def space_stats_csv(request):
    """A view that streams a large CSV file."""
    # Generate a sequence of rows. The range is based on the maximum number of
    # rows that can be handled by a single sheet in most spreadsheet
    # applications.
    rows = (["Row {}".format(idx), str(idx)] for idx in range(65536))
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows), content_type="text/csv")
	
    response['Content-Disposition'] = 'attachment; filename="space_stats.csv"'
    return response