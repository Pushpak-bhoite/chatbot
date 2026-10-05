def main():
    print("Hello from 15-claude-code!")


if __name__ == "__main__":
    main()


from agent import run_agent


def main():

    print("================================")
    print("       Mini Code Agent")
    print("================================")

    while True:

        user_input = input("\nYou: ")

        if user_input.lower in {"quit", "exit"}:
            break

        run_agent(user_input)


if __name__ == "__main__":
    main()