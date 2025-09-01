Financial Manager 
1. Introduction
The Financial Manager is a web-based Django application that allows users to record, monitor, and analyze their personal finances. It provides features for managing income and expenses, categorizing transactions, and generating summaries. The system’s primary goal is to help users maintain better control over their financial health.
________________________________________
2. Objectives
•	Provide secure user authentication (registration, login, logout).
•	Allow users to track transactions (income and expenses).
•	Enable users to edit and delete transactions.
•	Provide search and filter functionality for quick access to financial records.
•	Generate financial summaries and reports (balance, income vs. expenses).
•	Ensure the system is responsive and user-friendly.
________________________________________
3. Features
3.1 User Authentication & Registration
•	New users can register accounts with username, email, and password.
•	Existing users can log in and log out securely.
3.2 User Profile Management
•	Each user has a personal profile linked to their account.
•	Users can update details such as profile picture and bio.
3.3 Transaction Management
•	Users can add transactions as either:
o	Income (salary, investments, etc.)
o	Expenses (food, transport, bills, etc.)
•	Each transaction includes:
o	Title/Description
o	Amount
o	Category
o	Date
•	Transactions can be edited or deleted.
3.4 Financial Overview & Reports
•	Dashboard summary showing:
o	Total Income
o	Total Expenses
o	Net Balance (Income – Expenses)
•	Basic charts or tabular reports (Django templates rendering data from PostgreSQL).
3.5 Search & Filtering
•	Search transactions by keywords.
•	Filter by date range or category.
3.6 Responsive Design
•	Templates styled with CSS for a dark + light theme option.
•	Layout adapts for desktop and mobile devices.
________________________________________
4. Technology Stack
•	Backend Framework: Django (Python)
•	Frontend: HTML, CSS (with Django Template Language)
•	Database: PostgreSQL
•	Authentication: Django’s built-in auth system
________________________________________
5. Conclusion
The Financial Manager system combines Django’s robustness with PostgreSQL’s reliability to provide a secure, efficient, and user-friendly solution for personal financial tracking. With authentication, profile management, transaction handling, and reporting, users gain practical insights into their financial habits and can make better-informed decisions.

