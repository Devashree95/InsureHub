# Insurehub

# CS5614: DBMS Application for Insurance Company using Streamlit and PostgreSQL

# Team Members:
  Devashree Bhagwat​ (devashreeb@vt.edu) <br>
  Kanad Naleshwarkar​ (kanadn@vt.edu) <br>
  Shalini Rama​ (shalinir22@vt.edu) <br>
  Vasundhara Gowrishankar (vasundharag@vt.edu) <br>

# Overview
This project entails the development of a comprehensive database system tailored for an insurance
company. The system is designed to efficiently manage and streamline various aspects of insurance
operations, including policy management, payment processing, claim handling, and agent performance
tracking. It will feature a user-friendly interface that caters to different user types, including policyholders, relationship managers, and administrative staff. The system will centralize and automate key functions such as policy enrolment, premium payments, claim submissions, and performance analytics. This modernized approach aims to enhance the customer experience, optimize agent productivity, and provide the company with valuable insights for strategic decision-making.

# List of System Users
1. Policyholders (Insurers)
2. Relationship Managers (Agents)
3. Administrative Staff (Company)

# Functionalities for Each User
1) Policyholders (Insurers)
1. Browse insurance products.
2. View and manage personal policies.
3. Make premium payments.
4. File insurance claims.
5. Update personal and contact information.

2) Relationship Managers (Agents)
1. Access and manage assigned policyholder details.
2. Submit and manage claims on behalf of policyholders.
3. Monitor personal performance metrics and goals.
4. Access and provide policy details and product information.

3) Administrative Staff
1. Access and analyze agent performance metrics.
2. Create and manage insurance product listings.

# Installation
Clone the Repository: git clone https://version.cs.vt.edu/kanadn/insurehub.git <br>
Install Dependencies: pip install -r requirements.txt <br>
Set up PostgreSQL: Ensure you have PostgreSQL installed and running. The schema and sql dump files are added in '/data' foder. Import these files to set up local db. Update the database connection details in .env file. <br>
Run the Application: streamlit run .\Insurehub_Home.py <br>
