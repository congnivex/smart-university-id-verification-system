# Smart University ID & Verification System

A **Data Structures and Algorithms project** that simulates a **smart university ID verification and campus entry management system**.

The system manages student records, verifies IDs, records campus entries, and supports navigation between campus blocks using multiple **core data structures and algorithms**.

---

# Project Objective

The goal of this project is to demonstrate practical use of **multiple data structures and algorithms** in a real-world university management scenario.

The system allows administrators to:

* Store and manage student records
* Verify student IDs quickly
* Record and track campus entry logs
* Search student names efficiently
* Undo entry operations
* Find shortest paths between campus blocks

---

# Key Data Structures Used

| Data Structure | Purpose                          |
| -------------- | -------------------------------- |
| Hash Table     | Fast student ID lookup           |
| Linked List    | Collision handling in hash table |
| Trie           | Prefix-based student name search |
| Queue          | Manage entry logs                |
| Stack          | Undo last entry operation        |
| Graph          | Campus navigation                |

---

# Algorithms Implemented

### Hashing

Used for **fast student record lookup**.

Average Time Complexity:

| Operation | Complexity |
| --------- | ---------- |
| Insert    | O(1)       |
| Search    | O(1)       |
| Delete    | O(1)       |

---

### Linear Search

Used as a fallback searching method for small datasets.

Time Complexity:

O(n)

---

### Trie Prefix Search

Used for **auto-complete student name search**.

Time Complexity:

| Operation     | Complexity |
| ------------- | ---------- |
| Insert        | O(L)       |
| Prefix Search | O(L)       |

L = length of word

---

### Breadth First Search (BFS)

Used to calculate the **shortest path between campus blocks**.

Time Complexity:

O(V + E)

Where:

* V = number of vertices
* E = number of edges

---

# System Modules

## 1. Data Management Module

Responsibilities:

* Store student records
* Verify student IDs
* Maintain entry logs
* Support undo operations

Data Structures Used:

* Hash Table
* Linked List
* Queue
* Stack

---

## 2. Processing / Logic Module

Handles the core system logic including:

* Hash-based ID lookup
* Prefix-based name searching
* Campus navigation path finding
* Entry logging operations

Algorithms Used:

* Hashing
* Linear Search
* Trie Search
* BFS

---

## 3. User Interaction Module

A **menu-driven console interface** used for testing the core system functionality.

This interface allows users to interact with the system and perform operations such as adding records and searching.

---

# System Class Design

### StudentRecord

Attributes:

* id
* name
* department
* batch

Functions:

* getId()
* getName()
* getDepartment()
* getBatch()
* toString()

---

### LogEntry

Stores student entry information.

Attributes:

* studentId
* location
* timestamp

Functions:

* constructor
* toString()

---

### HashTable

Stores student records for fast ID verification.

Attributes:

* buckets (Array of LinkedLists)
* capacity
* size

Functions:

* hash()
* insertStudent()
* searchStudent()
* deleteStudent()

Uses **Linked List chaining** for collision handling.

---

### Trie

Used for prefix-based student name search.

Functions:

* insert()
* searchPrefix()
* getSuggestions()

---

### Queue

Used to maintain **chronological entry logs**.

Operations:

* enqueue()
* dequeue()
* isEmpty()
* display()

---

### Stack

Used to **undo the last entry operation**.

Operations:

* push()
* pop()
* peek()

---

### Graph

Represents the **campus layout**.

Functions:

* addBlock()
* addPath()
* bfsShortestPath()

---

# Menu Driven Demonstration

The system includes a **console-based menu** for testing:

```
1. Add Student Record
2. Delete Student Record
3. Search Student by ID
4. Search Student Name
5. Record Student Entry
6. View Entry Logs
7. Undo Last Entry
8. Exit
```

This menu demonstrates operations such as **insertion, deletion, searching, and traversal**.

---

# Test Cases

| Test Case      | Input         | Expected Output | Result |
| -------------- | ------------- | --------------- | ------ |
| Add Student    | Valid record  | Record added    | Passed |
| Duplicate ID   | Same ID again | Rejected        | Passed |
| Search Student | Valid ID      | Found           | Passed |
| Undo Entry     | Undo last log | Removed         | Passed |
| Empty Queue    | Dequeue       | Error message   | Passed |

---

# Edge Cases Handled

* Duplicate student IDs
* Undo operation on empty stack
* Queue traversal on empty log list
* Invalid student ID search

---

# Limitations

Current system limitations include:

* Console-based interface
* Partial system integration
* Static campus layout
* Limited input validation

---

# Future Improvements

Planned improvements include:

* Graphical user interface
* Complete module integration
* Improved validation and error handling
* Optimized data structure performance
* Real-time campus navigation system

---

# Author

Muskan Fatima
Artificial Intelligence Student

---

# License

This project is developed for **academic and educational purposes**.
