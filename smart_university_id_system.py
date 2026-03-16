import math
import time
from typing import List, Optional, Tuple


class Student:
    def __init__(self, student_id: int, name: str, department: str, batch: str):
        self.id = student_id
        self.name = name
        self.department = department
        self.batch = batch

    def __repr__(self) -> str:
        return f"{self.id} | {self.name} | {self.department} | {self.batch}"


class HashTableEntry:
    def __init__(self, key: int, value: Student):
        self.key = key
        self.value = value
        self.next: Optional["HashTableEntry"] = None


class HashTable:

    def __init__(self, initial_capacity: int = 11, load_factor: float = 0.75):
        self.capacity = initial_capacity
        self.size = 0
        self.load_factor = load_factor
        self.buckets: List[Optional[HashTableEntry]] = [None] * self.capacity

    def _hash(self, key: int) -> int:
        return abs(key) % self.capacity

    def _rehash_if_needed(self) -> None:
        if self.size / self.capacity < self.load_factor:
            return
        old_buckets = self.buckets
        self.capacity = self.capacity * 2 + 1
        self.buckets = [None] * self.capacity
        self.size = 0
        for head in old_buckets:
            node = head
            while node:
                self.insert_student(node.key, node.value.name, node.value.department, node.value.batch)
                node = node.next

    def insert_student(self, student_id: int, name: str, department: str, batch: str) -> bool:
        index = self._hash(student_id)
        head = self.buckets[index]
        node = head
        while node:
            if node.key == student_id:
                return False  # duplicate ID
            node = node.next
        new_entry = HashTableEntry(student_id, Student(student_id, name, department, batch))
        new_entry.next = head
        self.buckets[index] = new_entry
        self.size += 1
        self._rehash_if_needed()
        return True

    def search_student(self, student_id: int) -> Optional[Student]:
        index = self._hash(student_id)
        node = self.buckets[index]
        while node:
            if node.key == student_id:
                return node.value
            node = node.next
        return None

    def delete_student(self, student_id: int) -> bool:
        index = self._hash(student_id)
        node = self.buckets[index]
        prev = None
        while node:
            if node.key == student_id:
                if prev:
                    prev.next = node.next
                else:
                    self.buckets[index] = node.next
                self.size -= 1
                return True
            prev, node = node, node.next
        return False

    def list_students(self) -> List[Student]:
        students: List[Student] = []
        for head in self.buckets:
            node = head
            while node:
                students.append(node.value)
                node = node.next
        return students


class TrieNode:
    def __init__(self):
        self.children = {}
        self.words: List[str] = []  # store original-cased names ending here


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def _normalize(self, word: str) -> str:
        return word.strip().lower()

    def insert(self, word: str) -> None:
        normalized = self._normalize(word)
        node = self.root
        for ch in normalized:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.words.append(word)

    def search_prefix(self, prefix: str) -> bool:
        node = self._traverse(prefix)
        return node is not None

    def get_suggestions(self, prefix: str) -> List[str]:
        prefix = self._normalize(prefix)
        node = self._traverse(prefix)
        if not node:
            return []
        suggestions: List[str] = []
        self._collect(node, prefix, suggestions)
        return suggestions

    def _traverse(self, text: str) -> Optional[TrieNode]:
        text = self._normalize(text)
        node = self.root
        for ch in text:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def _collect(self, node: TrieNode, prefix: str, output: List[str]) -> None:
        for word in node.words:
            output.append(word)
        for ch, child in node.children.items():
            self._collect(child, prefix + ch, output)


class LogNode:
    def __init__(self, log: Tuple[int, str, float]):
        self.log = log
        self.next: Optional["LogNode"] = None


class LogQueue:

    def __init__(self):
        self.front: Optional[LogNode] = None
        self.rear: Optional[LogNode] = None
        self.length = 0

    def enqueue(self, log: Tuple[int, str, float]) -> None:
        node = LogNode(log)
        if not self.front:
            self.front = self.rear = node
        else:
            assert self.rear is not None
            self.rear.next = node
            self.rear = node
        self.length += 1

    def dequeue(self) -> Optional[Tuple[int, str, float]]:
        if not self.front:
            return None
        node = self.front
        self.front = node.next
        if not self.front:
            self.rear = None
        self.length -= 1
        return node.log

    def display_logs(self) -> List[Tuple[int, str, float]]:
        logs: List[Tuple[int, str, float]] = []
        node = self.front
        while node:
            logs.append(node.log)
            node = node.next
        return logs


class Graph:
    def __init__(self):
        self.adj = {}

    def add_block(self, name: str) -> None:
        if name not in self.adj:
            self.adj[name] = []

    def add_path(self, a: str, b: str, distance: float) -> None:
        self.add_block(a)
        self.add_block(b)
        self.adj[a].append((b, distance))
        self.adj[b].append((a, distance))

    def shortest_path(self, start: str, end: str) -> Tuple[float, List[str]]:
        if start not in self.adj or end not in self.adj:
            return math.inf, []
        distances = {node: math.inf for node in self.adj}
        prev = {}
        distances[start] = 0.0
        visited = set()
        while True:
            current = None
            current_distance = math.inf
            for node, dist in distances.items():
                if node not in visited and dist < current_distance:
                    current = node
                    current_distance = dist
            if current is None or current == end:
                break
            visited.add(current)
            for neighbor, weight in self.adj[current]:
                if neighbor in visited:
                    continue
                new_dist = distances[current] + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    prev[neighbor] = current
        if distances[end] is math.inf:
            return math.inf, []
        path = [end]
        while path[-1] != start:
            path.append(prev[path[-1]])
        path.reverse()
        return distances[end], path


class SmartUniversitySystem:
    def __init__(self):
        self.students = HashTable()
        self.trie = Trie()
        self.logs = LogQueue()
        self.graph = Graph()
        self._seed_data()

    def _seed_data(self) -> None:
        demo_students = [
            (101, "Awais Khan", "CS", "2025"),
            (102, "Alice Johnson", "Math", "2024"),
            (103, "Ahmad Raza", "EE", "2026"),
            (104, "Karen Smith", "Physics", "2023"),
            (105, "Khalid Hussain", "CS", "2025"),
        ]
        for sid, name, dept, batch in demo_students:
            self.students.insert_student(sid, name, dept, batch)
            self.trie.insert(name)

        demo_logs = [
            (101, "Library", time.time()),
            (102, "Cafeteria", time.time()),
            (103, "Main Gate", time.time()),
            (104, "Lab A", time.time()),
            (105, "Auditorium", time.time()),
        ]
        for log in demo_logs:
            self.logs.enqueue(log)

        blocks = ["Main Gate", "Library", "Cafeteria", "Lab A"]
        for b in blocks:
            self.graph.add_block(b)
        self.graph.add_path("Main Gate", "Library", 5)
        self.graph.add_path("Library", "Cafeteria", 3)
        self.graph.add_path("Cafeteria", "Lab A", 4)
        self.graph.add_path("Main Gate", "Lab A", 12)

    def add_student(self) -> None:
        try:
            sid = int(input("Enter student ID: "))
        except ValueError:
            print("Invalid ID.")
            return
        name = input("Enter name: ").strip()
        dept = input("Enter department: ").strip()
        batch = input("Enter batch: ").strip()
        if self.students.insert_student(sid, name, dept, batch):
            self.trie.insert(name)
            print("Student added.")
        else:
            print("Duplicate ID detected. Not added.")

    def verify_student(self) -> None:
        try:
            sid = int(input("Enter student ID to verify: "))
        except ValueError:
            print("Invalid ID.")
            return
        student = self.students.search_student(sid)
        if student:
            print("Valid ID:", student)
        else:
            print("Invalid or fake ID.")

    def search_by_name(self) -> None:
        prefix = input("Enter name prefix: ")
        suggestions = self.trie.get_suggestions(prefix)
        if suggestions:
            print("Matches:")
            for name in suggestions:
                print("-", name)
        else:
            print("No matches.")

    def log_entry(self) -> None:
        try:
            sid = int(input("Enter student ID: "))
        except ValueError:
            print("Invalid ID.")
            return
        location = input("Enter location: ").strip()
        timestamp = time.time()
        self.logs.enqueue((sid, location, timestamp))
        print("Entry logged.")

    def show_logs(self) -> None:
        logs = self.logs.display_logs()
        if not logs:
            print("No logs.")
            return
        for sid, location, ts in logs:
            print(f"{sid} @ {location} - {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))}")

    def shortest_path(self) -> None:
        start = input("Start block: ").strip()
        end = input("End block: ").strip()
        dist, path = self.graph.shortest_path(start, end)
        if math.isinf(dist):
            print("No path found.")
        else:
            print(f"Shortest distance: {dist} via {' -> '.join(path)}")

    def menu(self) -> None:
        options = {
            "1": self.add_student,
            "2": self.verify_student,
            "3": self.search_by_name,
            "4": self.log_entry,
            "5": self.show_logs,
            "6": self.shortest_path,
            "0": None,
        }
        while True:
            print("\nSmart University ID & Verification System")
            print("1. Add Student")
            print("2. Verify Student ID")
            print("3. Search Student by Name (Auto-complete)")
            print("4. Log Entry")
            print("5. Show Entry Logs")
            print("6. Shortest Path Between Blocks")
            print("0. Exit")
            choice = input("Select option: ").strip()
            if choice == "0":
                print("Goodbye.")
                break
            action = options.get(choice)
            if action:
                action()
            else:
                print("Invalid choice.")


def main() -> None:
    system = SmartUniversitySystem()
    system.menu()


if __name__ == "__main__":
    main()
