from flask_app.config.mysqlcontroller import connectToMySQL
import re
from flask import flash

DB = 'users_schema'

class Message:
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.user_id = data['user_id']
        self.target_id = data['target_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def send_message(cls, data):
        query = 'INSERT INTO messages (content, user_id, target_id) VALUES (%(content)s, %(user_id)s, %(target_id)s);'
        message_id = connectToMySQL(DB).query_db(query, data)
        return message_id

    @classmethod
    def get_messages(cls, data):
        query = 'SELECT * FROM messages WHERE target_id = %(user_id)s;'
        results = connectToMySQL(DB).query_db(query, data)
        messages = []
        for message in results:
            messages.append(cls(message))
        return messages

    @classmethod
    def get_messages_with_author(cls, data, user_or_target='target'):
        query = 'SELECT first_name, content, target_id, user_id, messages.created_at FROM users_schema.users '
        query += 'LEFT JOIN users_schema.messages ON users.id = user_id WHERE '
        if user_or_target == 'target':
            query += 'target_id = %(target_id)s;'
        else:
            query += 'user_id = %(user_id)s;'
        results = connectToMySQL(DB).query_db(query, data)
        return results
