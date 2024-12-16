from jpn_frlg_helper import cli_pidcalc, cli_adjustcalc


def main():
    while True:
        user_input = input("Calculate PID (0) / Calculate Adjustment (1): ")
        match user_input:
            case "0":
                return cli_pidcalc.main()
            case "1":
                return cli_adjustcalc.main()
            case _:
                continue


if __name__ == "__main__":
    main()