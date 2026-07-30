# simple-library
# Object-Oriented Library Management System

A simple, interactive Command Line Interface (CLI) application built with Python to demonstrate the core principles of Object-Oriented Programming (OOP): Abstraction, Encapsulation, Inheritance, and Polymorphism.

## 🚀 Features

*   **Interactive CLI Menu**: Continually loops and waits for user inputs.
*   **Search Catalogue**: Search physical books, journals, or digital collections by title or author.
*   **Borrowing Transaction**: Dynamically creates transaction objects to link members and library items.
*   **Extend Book Duration**: Easily extend the return deadline for active borrowed items.
*   **Return Item**: Processes returned physical items and updates their availability status in real-time.

## 🛠️ OOP Core Implementations

This system strictly applies 5 fundamental classes to address architectural scalability:
1.  **ItemPerpustakaan (Abstraction)**: Serves as an abstract base class forcing subclasses to implement core informational methods.
2.  **Buku & Jurnal (Inheritance)**: Physical subclasses inheriting main properties from the library item blueprint while adding custom attributes like ISBN and Volume.
3.  **KoleksiDigital (Polymorphism)**: Overrides specific item features to ensure electronic materials are always accessible via download links without locking their availability.
4.  **Anggota**: Defines user roles and identification mappings within the system.
5.  **Peminjaman (Encapsulation)**: Safeguards loan logs and dates using strict access control, ensuring no external functions can break transaction states illegally.

## 📋 Prerequisites & Installation

Make sure you have **Python 3.x** installed on your local computer.

1. Clone or download this repository.
2. Save the main script as `perpus.py`.
3. Open your terminal or Command Prompt, navigate to the folder, and run:
   ```bash
   python sistem-perpus.py
   ```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
