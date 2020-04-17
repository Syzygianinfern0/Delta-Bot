from utils.scrapers import get_new_results, is_already_exist, keep_a_record


def main():
    # gen = get_new_results("Prof")
    for thing in get_new_results("QxR"):
        if not is_already_exist("QxR", str(thing)):
            keep_a_record("QxR", str(thing))


if __name__ == "__main__":
    main()
