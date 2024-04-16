Task
Generate a Postgres query to answer [QUESTION]{user_question}[/QUESTION]

Instructions
If you cannot answer the question with the available database schema, return 'I do not know'
Database Schema
The query will run on a database with the following schema: {table_metadata_string}
For joins match the table parameters of the ones needed.

Answer
Given the database schema, here is the Postgres query that answers [QUESTION]{user_question}[/QUESTION] [SQL]