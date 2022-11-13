create_type_table = """
CREATE TABLE IF NOT EXISTS type (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
);
"""

create_settings_table = """
CREATE TABLE IF NOT EXISTS settings(
  id INTEGER PRIMARY KEY AUTOINCREMENT, 
  type INTEGER NOT NULL, 
  server TEXT NOT NULL, 
  query JSON NOT NULL,  
  time_limit INTEGER NOT NULL,
  time_out INTEGER NOT NULL,
  last_time DATATIME NOT NULL,   
  project TEXT NOT NULL, 
  FOREIGN KEY (type) REFERENCES type (id)
);
"""

create_error_history_table = """
CREATE TABLE IF NOT EXISTS error_history(
  id INTEGER PRIMARY KEY AUTOINCREMENT, 
  settings_id INTEGER NOT NULL, 
  error_time DATATIME NOT NULL,  
  log TEXT NOT NULL, 
  FOREIGN KEY (settings_id) REFERENCES settings (id)
);
"""

create_user_table = """
CREATE TABLE IF NOT EXISTS user(
  id INTEGER PRIMARY KEY AUTOINCREMENT, 
  user_id TEXT NOT NULL
);
"""
