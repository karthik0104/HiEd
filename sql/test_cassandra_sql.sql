CREATE KEYSPACE IF NOT EXISTS thread_ks WITH REPLICATION = { 'class' : 'NetworkTopologyStrategy', 'datacenter1' : 3 };

USE thread_ks;

CREATE TABLE discussion_thread (id uuid, group_id int, user_id int, title text, content text, time1 timeuuid,
PRIMARY KEY (group_id, time1)) WITH CLUSTERING ORDER BY (time1 DESC);

CREATE TABLE thread_reply (id uuid, discussion_thread_id uuid, user_id int, content text, time1 timeuuid,
PRIMARY KEY (discussion_thread_id, time1)) WITH CLUSTERING ORDER BY (time1 DESC);

CREATE TABLE group_follower (id uuid, group_id int, user_id int, time1 timeuuid,
PRIMARY KEY (group_id, time1) WITH CLUSTERING ORDER BY (time1 DESC);