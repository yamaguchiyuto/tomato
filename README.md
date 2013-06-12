Landmark-Based User Location Inference
======================
An implementation of a user location inference method.  
If you want to know more, please refer to our paper.

Usage
------
### Prepare DB ###
    $ mysql -u username -p
    mysql> create database dbname;
    mysql> quit;
    Bye
    $ mysql -u username -p dbname < tomato/sql/tomato.sql

### Structures of tables ###
    mysql> show tables;
    +-------------------+
    | Tables_in_tomato2 |
    +-------------------+
    | dominance         |
    | graph             |
    | users             |
    +-------------------+

    mysql> show fields from dominance;
    +------------+------------+------+-----+---------+-------+
    | Field      | Type       | Null | Key | Default | Extra |
    +------------+------------+------+-----+---------+-------+
    | id         | bigint(20) | NO   | PRI | 0       |       |
    | type       | int(11)    | NO   | PRI | 0       |       |
    | centrality | float      | YES  |     | NULL    |       |
    | variance   | float      | YES  |     | NULL    |       |
    | latitude   | float      | YES  |     | NULL    |       |
    | longitude  | float      | YES  |     | NULL    |       |
    +------------+------------+------+-----+---------+-------+

    mysql> show fields from graph;
    +--------+------------+------+-----+---------+-------+
    | Field  | Type       | Null | Key | Default | Extra |
    +--------+------------+------+-----+---------+-------+
    | src_id | bigint(20) | NO   | PRI | 0       |       |
    | dst_id | bigint(20) | NO   | PRI | 0       |       |
    +--------+------------+------+-----+---------+-------+

    mysql> show fields from users;
    +-------------+--------------+------+-----+---------+-------+
    | Field       | Type         | Null | Key | Default | Extra |
    +-------------+--------------+------+-----+---------+-------+
    | id          | bigint(20)   | NO   | PRI | 0       |       |
    | screen_name | varchar(100) | YES  |     | NULL    |       |
    | latitude    | float        | YES  |     | NULL    |       |
    | longitude   | float        | YES  |     | NULL    |       |
    +-------------+--------------+------+-----+---------+-------+

### Prepare db.conf ###
``db.conf`` is used by ``lib/db.py`` to connect to DB.

    $ cat tomato/data/db.conf
    hostname
    dbusername
    dbpassword
    dbname

### Calculate dominance distribution of all users ###
    $ python calculate_dominance_distribution.py
Results are inserted into ``dominance`` table.

### Infer ###
    $ python lmm.py [c0]  # c0 is a threshold value of the centrality constraint.
Results are printed out to stdout.

Output
------
### Output format ###
    {'user_id': 481102014,
     'inferred_location': (36.056, 140.026),
     'confidence': 0.045,
     'actual_location': (36.086, 140.078)
    }
If a user's actual location is unknown, ``actual_location`` value is ``None``.  
``confidence`` indicates how likely the corresponding user's home location is at ``inferred_location``.
