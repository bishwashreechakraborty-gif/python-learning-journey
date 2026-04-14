# 🐍 Python Beginner to Intermediate Practice Repository

This repository contains a structured collection of **20 Python programs** designed for beginners to build a strong foundation in programming. It starts with basic syntax and gradually moves toward problem-solving and mini-projects.

---

## 📂 Project Structure

### 🔰 Basics

| File                         | Description                                                    |
| ---------------------------- | -------------------------------------------------------------- |
| `hello_world.py`             | Your first Python program using `print()`                      |
| `variables_and_datatypes.py` | Learn strings, integers, floats, and booleans                  |
| `input_and_conditions.py`    | User input with `input()` and decision making (`if/elif/else`) |
| `loops.py`                   | `for`, `while` loops with patterns and `break/continue`        |
| `lists.py`                   | Lists, indexing, slicing, sorting, list comprehensions         |
| `functions.py`               | Functions, arguments, return values, recursion                 |
| `dictionaries.py`            | Key-value pairs and dictionary operations                      |
| `strings.py`                 | String methods, formatting, palindrome check                   |
| `file_handling.py`           | Reading and writing `.txt` files                               |
| `classes_intro.py`           | Basics of OOP: classes and objects                             |

---

### 🚀 Intermediate Concepts

| File                         | Description                            |
| ---------------------------- | -------------------------------------- |
| `modules_and_packages.py`    | Using built-in and custom modules      |
| `exception_handling.py`      | Error handling with try-except-finally |
| `simple_calculator.py`       | Basic calculator using functions       |
| `random_numbers.py`          | Random number generation               |
| `guess_the_number.py`        | Interactive number guessing game       |
| `basic_file_project.py`      | File read/write mini project           |
| `simple_oop_project.py`      | OOP example using a Student class      |
| `basic_lambda_map_filter.py` | Functional programming basics          |
| `datetime_example.py`        | Working with date and time             |
| `mini_project_todo.py`       | Simple command-line To-Do list         |

---

## 🎯 Learning Outcomes

By completing this repository, you will:

* Understand Python syntax and fundamentals
* Gain experience with control structures and data types
* Learn basic Object-Oriented Programming (OOP)
* Work with files and error handling
* Build small real-world projects
* Improve logical thinking and problem-solving skills

---

## 🛠️ How to Run

1. Install Python (>= 3.x)
2. Clone this repository:

   ```bash
   git clone https://github.com/bishwashreechakraborty-gif/python-learning-journey.git
   ```
3. Navigate to the folder:

   ```bash
   cd python-learning-journey
   ```
4. Run any file:

   ```bash
   python filename.py
   ```

---

## 📌 Future Improvements

* Add GUI projects (Tkinter)
* Add data analysis using Pandas
* Add more advanced problem-solving questions
* Build real-world applications

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork this repository and submit a pull request.

---

## ⭐ Support

If you found this repository helpful, please consider giving it a ⭐ on GitHub!

---

## 📦 Custom Module Explanation (`mymodule.py`)

This repository includes an example of creating and using a **custom Python module**.

---

### 🔹 Step 1: Create the module

File: `mymodule.py`

```python
def greet(name):
    return f"Hello, {name}"
```

---

### 🔹 Step 2: Use the module

File: `11_modules_and_packages.py`

```python
# Make sure mymodule.py is in the same folder

import mymodule

print(mymodule.greet("Bishwashree"))
```

---

### ⚠️ Important Note

* `mymodule.py` must be in the **same directory** as `11_modules_and_packages.py`
* Otherwise, Python will raise:

  ```
  ModuleNotFoundError: No module named 'mymodule'
  ```

---

### ✅ Output

```
Hello, Bishwashree
```

### Developed by Bishwashree Chakraborty
