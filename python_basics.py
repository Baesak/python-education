import re

# 1 Hello world
print('1 Hello world')
print("Hello, world!")

# 2 Variables and Types
my_string = "hello"
my_float = 10.0
my_int = 20

# 3 Lists
numbers = []
strings = []
names = ["John", "Eric", "Jessica"]

numbers.append(1)
numbers.append(2)
numbers.append(3)

strings.append("hello")
strings.append("world")

second_name = names[1]

# 4 Basic Operators
x = object()
y = object()


x_list = [x] * 10
y_list = [y] * 10
big_list = x_list + y_list

# 5 String formatting

data = ("John", "Doe", 53.44)
format_string = f"Hello {data[0]} {data[1]}. Your current balance is {data[2]}"

print(format_string)

# 6 Basic String Operators
s = "Strings are awesome!"
# Length should be 20
print("Length of s = %d" % len(s))

# First occurrence of "a" should be at index 8
print("The first occurrence of the letter a = %d" % s.index("a"))

# Number of a's should be 2
print("a occurs %d times" % s.count("a"))

# Slicing the string into bits
print("The first five characters are '%s'" % s[:5]) # Start to 5
print("The next five characters are '%s'" % s[5:10]) # 5 to 10
print("The thirteenth character is '%s'" % s[12]) # Just number 12
print("The characters with odd index are '%s'" %s[1::2]) #(0-based indexing)
print("The last five characters are '%s'" % s[-5:]) # 5th-from-last to end

# Convert everything to uppercase
print("String in uppercase: %s" % s.upper())

# Convert everything to lowercase
print("String in lowercase: %s" % s.lower())

# Check how a string starts
if s.startswith("Str"):
    print("String starts with 'Str'. Good!")

# Check how a string ends
if s.endswith("ome!"):
    print("String ends with 'ome!'. Good!")

# Split the string into three separate strings,
# each containing only a word
print("Split the words of the string: %s" % s.split(" "))


# 7 Conditions
number = 16
second_number = 0
first_array = [1, 2, 3]
second_array = [1, 2]

if number > 15:
    print("1")

if first_array:
    print("2")

if len(second_array) == 2:
    print("3")

if len(first_array) + len(second_array) == 5:
    print("4")

if first_array and first_array[0] == 1:
    print("5")

if not second_number:
    print("6")


# 8 Loops

numbers = [
    951, 402, 984, 651, 360, 69, 408, 319, 601, 485, 980, 507, 725, 547, 544,
    615, 83, 165, 141, 501, 263, 617, 865, 575, 219, 390, 984, 592, 236, 105, 942, 941,
    386, 462, 47, 418, 907, 344, 236, 375, 823, 566, 597, 978, 328, 615, 953, 345,
    399, 162, 758, 219, 918, 237, 412, 566, 826, 248, 866, 950, 626, 949, 687, 217,
    815, 67, 104, 58, 512, 24, 892, 894, 767, 553, 81, 379, 843, 831, 445, 742, 717,
    958, 609, 842, 451, 688, 753, 854, 685, 93, 857, 440, 380, 126, 721, 328, 753, 470,
    743, 527
]

# your code goes here
for number in numbers:
    if number == 237:
        break

    elif number % 2 == 1:
        print(number)


# 9 Functions
# 1
# Modify this function to return a list of strings as defined above
def list_benefits():
    return "More organized code", "More readable code", "Easier code reuse", \
           "Allowing programmers to share and connect code together"


# Modify this function to concatenate to each benefit - " is a benefit of functions!"
def build_sentence(benefit):
    return f"{benefit} is a benefit of functions!"


def name_the_benefits_of_functions():
    list_of_benefits = list_benefits()
    for benefit in list_of_benefits:
        print(build_sentence(benefit))


name_the_benefits_of_functions()


# 2
# edit the functions prototype and implementation
def foo(a, b, c, *args):
    return len(args)


def bar(a, b, c, **kwargs):
    return kwargs["magicnumber"] == 7


# 11 Dictionaries
phonebook = {
    "John": 938477566,
    "Jack": 938377264,
    "Jill": 947662781
}

# your code goes here
phonebook.update({"Jake": 938273443})
del phonebook["Jill"]


# 12 Sets
a = ["Jake", "John", "Eric"]
b = ["John", "Jill"]

A = set(a)
B = set(b)

print(A.difference(B))


# 15 Modules and Packages

# Your code goes here
find_members = [member for member in dir(re) if "find" in member]

print(sorted(find_members))
