create_Db = "CREATE DATABASE if not exists MainDB"

create_type_table = """
CREATE TABLE if not exists type 
  (id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  name TEXT NOT NULL);
"""

create_settings_table = """
CREATE TABLE if not exists settings(
  id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  type INTEGER NOT NULL, 
  server TEXT NOT NULL, 
  query JSON NOT NULL,  
  time_limit INTEGER NOT NULL,
  time_out INTEGER NOT NULL,
  last_time timestamp NOT NULL,   
  project TEXT NOT NULL, 
  FOREIGN KEY (type) REFERENCES type (id)
);
"""

create_error_history_table = """
CREATE TABLE if not exists error_history(
  id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  settings_id INTEGER NOT NULL, 
  error_time timestamp NOT NULL,  
  log TEXT NOT NULL, 
  FOREIGN KEY (settings_id) REFERENCES settings (id)
);
"""

create_user_table = """
CREATE TABLE if not exists users(
  id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  user_id TEXT NOT NULL
);
"""
