import mariadb
import sys
from database_config import db_config

try:
    conn = mariadb.connect(**db_config)
    cursor = conn.cursor()
    print("🔌 Connected to Database")

    # 1. Create 'users' table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50),
        password VARCHAR(100),
        email VARCHAR(100),
        role VARCHAR(20)
    )
    """)
    print("✅ Table 'users' created.")

    # 2. Create 'systems' table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS systems (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50)
    )
    """)
    cursor.execute("INSERT IGNORE INTO systems (id, name) VALUES (1, 'AEGIS_CORE')")
    print("✅ Table 'systems' created.")

    # 3. Create 'incident_types' table (WITH severity_level)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS incident_types (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50),
        severity_level VARCHAR(20)
    )
    """)
    cursor.execute("INSERT IGNORE INTO incident_types (id, name, severity_level) VALUES (1, 'LOGIN_ATTEMPT', 'LOW'), (2, 'WAF_BLOCK', 'MEDIUM'), (3, 'CRITICAL_BREACH', 'HIGH')")
    print("✅ Table 'incident_types' created.")

    # 4. Create 'incidents' table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS incidents (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(100),
        description TEXT,
        system_id INT,
        incident_type_id INT,
        risk_score INT,
        ip_address VARCHAR(45),
        country VARCHAR(50) DEFAULT 'Unknown',
        status VARCHAR(20) DEFAULT 'OPEN',
        reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (system_id) REFERENCES systems(id),
        FOREIGN KEY (incident_type_id) REFERENCES incident_types(id)
    )
    """)
    print("✅ Table 'incidents' created.")

    # 5. INSERT DUMMY DATA FOR USERS
    cursor.execute("""
    INSERT IGNORE INTO users (id, username, password, email, role) 
    VALUES 
    (1, 'admin', 'SuperSecretAdminPass!', 'admin@aegis.corp', 'admin'),
    (2, 'prateek', 'root', 'prateek@dev.local', 'user'),
    (3, 'ceo_dave', 'golf_is_life', 'dave@aegis.corp', 'executive')
    """)
    print("✅ Dummy Users inserted.")

    conn.commit()
    conn.close()
    print("🚀 DATABASE FULLY REPAIRED.")

except mariadb.Error as e:
    print(f"❌ Error: {e}")