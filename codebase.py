
import pandas as pd

# Step 1: Read student data from CSV file
def load_data():
    try:
        df = pd.read_csv("students.csv")

        # Standardize column names
        df.columns = [
            col.strip().lower().replace(" ", "").replace("(", "").replace(")", "").replace("%", "").replace("_", "")
            for col in df.columns
        ]

        required = ["name", "marks", "income", "attendance"]

        if not all(col in df.columns for col in required):
            print("Error: CSV must contain Name, Marks, Income and Attendance columns.")
            return None

        df = df[required].copy()

        # Convert numeric columns
        for col in ["marks", "income", "attendance"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # Identify invalid rows
        invalid = (
            df["name"].isna()
            | (df["name"].astype(str).str.strip() == "")
            | df["marks"].isna()
            | df["income"].isna()
            | df["attendance"].isna()
            | (df["marks"] < 0)
            | (df["marks"] > 100)
            | (df["income"] < 0)
            | (df["attendance"] < 0)
            | (df["attendance"] > 100)
        )

        for index in df[invalid].index:
            print(f"Invalid or missing data in row {index + 2}. Row skipped.")

        df = df[~invalid].copy()

        return df

    except FileNotFoundError:
        print("Error: students.csv file not found!")
        return None

    except Exception as e:
        print("Error:", e)
        return None


# Step 2: Check scholarship eligibility
def check_scholarship(row):

    if row["attendance"] < 75:
        return "Not Eligible", 0

    elif row["marks"] >= 75 and row["income"] <= 500000:
        return "Full", 50000

    elif row["marks"] >= 60 and row["income"] <= 2000000:
        return "Partial", 25000

    else:
        return "Not Eligible", 0


# Step 3: Analyze student records
def analyze_students(df):

    results = df.copy()

    results[["Scholarship", "Amount"]] = results.apply(
        lambda row: pd.Series(check_scholarship(row)),
        axis=1
    )

    return results


# Step 4: Display all student results
def display_results(results):

    print("\n========== STUDENT SCHOLARSHIP RESULTS ==========")

    for _, row in results.iterrows():
        print(
            f'{row["name"]} | {row["Scholarship"]} | '
            f'Rs. {row["Amount"]}'
        )


# Step 5: Display summary
def display_summary(results):

    eligible = results[
        results["Scholarship"] != "Not Eligible"
    ]

    not_eligible = results[
        results["Scholarship"] == "Not Eligible"
    ]

    full = results[results["Scholarship"] == "Full"]
    partial = results[results["Scholarship"] == "Partial"]

    total_amount = results["Amount"].sum()

    print("\n========== SCHOLARSHIP SUMMARY ==========")

    print("Total Students:", len(results))
    print("Eligible Students:", len(eligible))
    print("Not Eligible Students:", len(not_eligible))
    print("Full Scholarships:", len(full))
    print("Partial Scholarships:", len(partial))
    print("Total Scholarship Amount: Rs.", total_amount)

    if len(eligible) > 0:
        print(
            "Average Marks of Eligible Students:",
            f'{eligible["marks"].mean():.2f}'
        )
    else:
        print("Average Marks of Eligible Students: 0")


# Step 6: Filter students by minimum marks
def filter_students(results):

    try:
        minimum = float(input("Enter minimum marks: "))

        filtered = results[results["marks"] >= minimum]

        print("\nStudents scoring", minimum, "or above:")

        if filtered.empty:
            print("No students found.")
        else:
            print(filtered[
                ["name", "marks", "Scholarship", "Amount"]
            ].to_string(index=False))

    except ValueError:
        print("Please enter a valid number.")


# Main program
def main():

    df = load_data()

    if df is None:
        return

    if df.empty:
        print("No valid student records available.")
        return

    results = analyze_students(df)

    while True:

        print("\n======= STUDENT SCHOLARSHIP ANALYZER =======")
        print("1. Display Eligibility Results")
        print("2. Display Scholarship Summary")
        print("3. Filter Students by Minimum Marks")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            display_results(results)

        elif choice == "2":
            display_summary(results)

        elif choice == "3":
            filter_students(results)

        elif choice == "4":
            print("Thank you for using Scholarship Analyzer!")
            break

        else:
            print("Invalid choice! Please try again.")


# Execute program
if __name__ == "__main__":
    main()
