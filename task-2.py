def generate_table():
    for i in range(1, 11):
        for j in range(1, 11):
            print(f"{i*j:4}", end="")
        print()

def main():
    example = generate_table()

if __name__ == '__main__':
    main()