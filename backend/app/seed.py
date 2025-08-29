import sys
from .database import engine
import json

def create_tables(conn):
    try:
        with open('backend/app/schema.sql', 'r') as f:
            schema = f.read()
        conn.executescript(schema)
        print("Tables created successfully based on schema.sql.")
    except Exception as e:
        print(f"ERROR: Failed to create tables: {e}", file=sys.stderr)
        raise

def seed_data(conn):
    cursor = conn.cursor()

    profile_data = (1, 'Vaibhav Rohilla', 'vaibhavrohilla03@gmail.com')

    links_data = [
        ('LinkedIn', 'https://www.linkedin.com/in/vaibhav-rohilla-097656255/'),
        ('GitHub', 'https://github.com/vaibhavrohilla-03'),
        ('LeetCode', 'https://leetcode.com/u/vaibhavrohilla03/')
    ]

    skills_data = [
        ('Python', 1), ('C++', 1), ('C#', 1), ('Unity', 1), ('Unreal Engine', 1),
        ('CMake', 0), ('SQL', 0), ('.NET', 0), ('AWS', 0), ('Firebase', 0),
        ('Git', 0), ('Perforce', 0), ('ASP.NET', 0), ('ARCore', 0),
        ('OpenXR', 0), ('ROS2', 0), ('SQLite', 0), ('ChromaDB', 0), ('Langchain', 0)
    ]

    categories_data = [
        ('AR/VR Development',),  
        ('.NET Development',),   
        ('Game Development',),   
        ('Backend and AI',),      
        ('Cloud Computing',),    
        ('QuantFinance',),       
        ('General',)              
    ]

    education_data = [
        ('Manipal University Jaipur', 'B.Tech in Computer Science and Engineering', '2022-08-01', '2026-05-31')
    ]

    work_experience_data = [
        ('EdCIL (India) Limited (Ministry of Education, GoI)', '.Net Developer Intern', '2025-05-01', '2025-07-31',
         'Architected a reusable, secure RESTful API for Aadhaar verification by developing a dedicated class library, standardizing the authentication process across multiple government portals. Developed and deployed an interactive chatbot for the official "Study in India" portal. Engineered the chatbot\'s backend to log and analyze user interactions, implementing an admin panel with an automated system for generating daily user activity reports.'),
        ('AIC (Atal Incubation Center), Manipal University Jaipur', 'AR/VR Developer Intern', '2024-11-01', None,
         'Developing AR/VR content for clients using Unreal Engine and Unity, enhancing interactive experiences with C++ and C#. Collaborating with startups at the incubation center, providing technical guidance on implementing AR/VR solutions. Conducting seminars and workshops for university freshers on Unity, Unreal Engine, and fundamental XR development concepts.'),
        ('Constituents AI And Technology Private Limited', 'Unity Developer Intern', '2023-10-01', '2024-01-31',
         'Developed building modules for a VR EdTech platform, enhancing the creation of interactive educational content in Unity with C# and XR SDKs. Optimized the existing VR content pipeline, reducing development time by 40% through improved workflow automation and scene management. Integrated custom tools and asset management systems to streamline the process of creating immersive learning experiences.')
    ]

    projects_data = [
        ('AR Campus Navigation using Google Cloud Anchors',
         'Developed an AR indoor navigation system using Google’s Persistent Cloud Anchors in Unity to provide real-time navigation assistance. Implemented a Firebase backend server to manage anchors and route storage. Designed a user-friendly interface and integrated QR code generation for retrieving routes.',
         json.dumps({"github": "https://github.com/vaibhavrohilla-03/AR_Nav2"})),
        ('Web Scraper & RAG Chatbot',
         'Developed a Retrieval-Augmented Generation (RAG) chatbot capable of answering queries using a dynamically generated knowledge base by leveraging a Large Language Model (LLM). Implemented a modular web scraper with Beautiful Soup to populate a ChromaDB vector database. Engineered a content retrieval pipeline to supply relevant context to the model.',
         json.dumps({"github": "https://github.com/vaibhavrohilla-03/webscrape_ragchatbot"})),
        ('TurtleSim Motion Controller',
         'Developed a ROS 2 node in C++ to control a virtual turtle in Turtle Sim using geometry_msgs/Twist. Utilized ROS 2 timers and publishers to automate movement without manual input. Built and launched using CMake, ensuring a modular and scalable architecture.',
         json.dumps({"github": "https://github.com/vaibhavrohilla-03/TurtleSim"})),
        ('Option Strategy Backtesting Engine (Work in Progress)',
         'A high-performance engine for backtesting financial option strategies. Built with C++ and CMake, and utilizing Python for scripting and analysis.',
         json.dumps({}))
    ]
    
    work_experience_categories_data = [
        (1, 2), (1, 4), # EdCIL -> .NET Development, Backend and AI
        (2, 1), (2, 3), # AIC -> AR/VR, Game Development
        (3, 1), (3, 3)  # Constituents AI -> AR/VR, Game Development
    ]

    project_categories_data = [
        (1, 1), (1, 5), # AR Nav -> AR/VR, Cloud Computing
        (2, 4),         # RAG Chatbot -> Backend and AI
        (3, 7),         # TurtleSim -> General                                                 (EK BAAR REVIEW MAAR LIYO ISKO WAPIS)
        (4, 6)          # Option Backtesting Engine -> QuantFinance
    ]

    project_skills_data = [
        # Project 1: AR Campus Navigation -> Unity, C#, Firebase, ARCore
        (1, 4), (1, 3), (1, 10), (1, 14),
        # Project 2: Web Scraper & RAG Chatbot -> Python, ChromaDB, Langchain
        (2, 1), (2, 18), (2, 19),                                                                    #(EK BAAR REVIEW MAAR LIYO ISKO WAPIS)
        # Project 3: TurtleSim Motion Controller -> C++, ROS2, CMake
        (3, 2), (3, 16), (3, 6),
        # Project 4: Option Strategy Backtesting Engine -> C++, Python, CMake
        (4, 2), (4, 1), (4, 6)
    ]

    try:
        print("Seeding data...")
        cursor.execute("INSERT INTO m_profile (id, name, email) VALUES (?, ?, ?);", profile_data)
        cursor.executemany("INSERT INTO links (name, url) VALUES (?, ?);", links_data)
        cursor.executemany("INSERT INTO skills (name, is_top_skill) VALUES (?, ?);", skills_data)
        cursor.executemany("INSERT INTO categories (name) VALUES (?);", categories_data)
        cursor.executemany("INSERT INTO education (institution, degree, start_date, end_date) VALUES (?, ?, ?, ?);", education_data)
        cursor.executemany("INSERT INTO work_experience (company, position, start_date, end_date, description) VALUES (?, ?, ?, ?, ?);", work_experience_data)
        cursor.executemany("INSERT INTO projects (title, description, links) VALUES (?, ?, ?);", projects_data)
        cursor.executemany("INSERT INTO project_categories (project_id, category_id) VALUES (?, ?);", project_categories_data)
        cursor.executemany("INSERT INTO work_experience_categories (work_experience_id, category_id) VALUES (?, ?);", work_experience_categories_data)
        cursor.executemany("INSERT INTO project_skills (project_id, skill_id) VALUES (?, ?);", project_skills_data)
        conn.commit()
        print("Seeding complete. Data committed.")
    except Exception as e:
        print(f"ERROR: An error occurred during seeding: {e}", file=sys.stderr)
        conn.rollback()
        raise

if __name__ == "__main__":
    print("Starting database seeding process.")
    connection = engine.raw_connection()
    try:
        create_tables(connection)
        seed_data(connection)
    finally:
        connection.close()
        print("Database connection closed.")