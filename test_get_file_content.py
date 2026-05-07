from functions.get_file_content import get_file_content


def main():
    print("calculator/main.py :")
    print(get_file_content("calculator", "main.py"))
    print('"calculator", "pkg/calculator.py"')
    print(get_file_content("calculator", "pkg/calculator.py"))
    print('"calculator", "/bin/cat"')
    print(get_file_content("calculator", "/bin/cat"))
    print('"calculator", "pkg/does_not_exist.py"')
    print(get_file_content("calculator", "pkg/does_not_exist.py"))


if __name__ == "__main__":
    main()
