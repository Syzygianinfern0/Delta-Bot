def keep_a_record(uploader: str, record):
    """
    :param uploader: uploader name mentioned in the url to the profile of the uploader
    :param record: this is used to pevent posting same torrent again and again.
     It is adviced to use the url property as the record
    :return: None
    """
    with open(uploader, "a") as file:
        file.write(record + "\n")


def is_already_exist(fname: str, record) -> bool:
    """
    :param uploader: uploader name mentioned in the url to the profile of the uploader
    :param record: this is used to pevent posting same torrent again and again.
     It is adviced to use the url property as the record
    :return: True when the last kept record is equal to the current record.
     False if doesnt match. False means search result is new.
    :raise: if the file not found
    """
    with open(fname, "r") as file:
        try:
            if file.readline() == record:
                return True
            else:
                return False
        except FileNotFoundError:
            open(fname, 'a').close()
