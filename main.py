from test import get_new_results, is_already_exist, keep_a_record


def main():
    # gen = get_new_results("Prof")
    for thing in get_new_results("Prof"):
        print(thing)


if __name__ == "__main__":
    main()
