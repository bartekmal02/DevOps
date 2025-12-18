def calculate_bmi(weight: float, height: float):
    weight = float(input("Podaj swoją wage w [kg]: "))
    height = float(input("Podaj swój wzrost w [cm]: "))

    BMI = weight / (height / 100) ** 2
    print(f"Twoje BMI: {BMI}")

    if BMI < 18.5:
        print("Masz niedowagę")
    elif BMI >= 18.5 and BMI <= 25:
        print("Waga prawidłowa")
    elif BMI >= 25 and BMI <= 30:
        print("Masz nadwage")
    else:
        print("Masz otyłość")

def main():
    example = calculate_bmi(weight=75.6, height=179.5)

if __name__ == "__main__":
    main()