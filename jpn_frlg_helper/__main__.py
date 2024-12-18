from jpn_frlg_helper import rngfinder, cli_pidcalc, cli_adjustcalc


def main():
    while True:
        user_input = input("Search RNG (0) / Calculate PID (1) / Calculate Adjustment (2): ")
        match user_input:
            case "0":
                return rngfinder.main()
            case "1":
                return cli_pidcalc.main()
            case "2":
                return cli_adjustcalc.main()
            case _:
                continue


if __name__ == "__main__":
    main()