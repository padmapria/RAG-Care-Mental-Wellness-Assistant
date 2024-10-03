USE rag_db;

CREATE TABLE requests (
    id VARCHAR(255) NOT NULL,  -- Assuming 'id' is a UUID or some other string identifier
    question TEXT NOT NULL,    -- 'question' is stored as text
    answer TEXT NOT NULL,      -- 'answer' is stored as text
    model_used VARCHAR(100),   -- Assuming 'model_used' is a string, like a model name or version
    response_time_in_seconds FLOAT,       -- 'response_time' in seconds, stored as a float
    relevance VARCHAR(16),      -- 'relevance' can be an integer (e.g., 1-5 or similar)
	relevance_expl VARCHAR(500),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- timestamp with default 
    PRIMARY KEY (id)           -- 'id' as the primary key
);
			
CREATE TABLE feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_id VARCHAR(255) NOT NULL,
    feedback TINYINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (question_id)
);
