import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(f"csv/export/{sys.argv[1]}", "x") as export_file:
            pass
